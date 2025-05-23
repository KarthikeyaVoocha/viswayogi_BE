from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import PatientProfile
from user_profile.decorators import authenticate_user_session
from user_profile.models import UserProfile
from django.utils.timezone import now
from django.db.models import Count
from datetime import datetime


HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.TYPE_STRING),
}

class FetchPatientsView(APIView):
    @swagger_auto_schema(
        operation_description="Fetch patients",
        manual_parameters=[HEADER_PARAMS['access_token']],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_params": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Authentication-related parameters",
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Authenticated user's ID"),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token"),
                    },
                    required=["user_id", "refresh_token"],
                ),
                "payload": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Appointment details",
                    properties={
                        "date": openapi.Schema(type=openapi.TYPE_STRING, description="date"),
                        "month": openapi.Schema(type=openapi.TYPE_STRING, description="month"),
                        "year": openapi.Schema(type=openapi.TYPE_STRING, description="year")
                    },
                    required=[],
                ),
            },
            required=["auth_params", "payload"],
        ),
        responses={
            200: openapi.Response(
                "Doctors fetched successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "doctors": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description="List of doctors",
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's User ID"),
                                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's full name"),
                                    "email": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's email"),
                                    "phone_no": openapi.Schema(type=openapi.TYPE_STRING, description="Doctor's phone number"),
                                },
                            ),
                        ),
                    },
                ),
            ),
            400: "Validation errors",
        },
    )
    @authenticate_user_session
    def post(self, request):
            try:
                # Get parameters from request (GET or POST as per your API)
                payload = request.data.get('payload', {})
                day_str = payload.get('date')      # Format: YYYY-MM-DD
                month_str = payload.get('month')    # Format: 1 to 12
                year_str = payload.get('year')      # Format: YYYY


                # Convert inputs to integers if present
                day = int(day_str) if day_str else None
                month = int(month_str) if month_str else None
                year = int(year_str) if year_str else None

                # Validate and build filtering date logic
                filter_mode = None
                filter_date = None

                if day and month and year:
                    # Full date
                    try:
                        filter_date = datetime(year, month, day).date()
                        filter_mode = "daily"
                    except ValueError:
                        return Response({"error": "Invalid day/month/year combination."}, status=400)
                elif month and year:
                    filter_mode = "monthly"
                elif year:
                    filter_mode = "yearly"
                else:
                    # Default to today's date
                    filter_date = now().date()
                    filter_mode = "daily"

                # Get all doctors
                doctors = UserProfile.objects.filter(role="doctor").values('designation', 'user_id')
                designation_counts = {}

                for doctor in doctors:
                    designation = doctor["designation"]
                    if designation not in designation_counts:
                        designation_counts[designation] = 0

                    queryset = PatientProfile.objects.filter(user_id=doctor["user_id"])

                    # Apply filter
                    if filter_mode == "daily":
                        queryset = queryset.filter(added_date__date=filter_date)
                    elif filter_mode == "monthly":
                        queryset = queryset.filter(
                            added_date__month=month,
                            added_date__year=year
                        )
                    elif filter_mode == "yearly":
                        queryset = queryset.filter(added_date__year=year)

                    designation_counts[designation] += queryset.count()

                return Response(designation_counts, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({"success": False, "error": str(e)}, status=500)
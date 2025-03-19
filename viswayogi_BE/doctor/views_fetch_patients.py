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
                    description="payload for fetching patient name",
                    properties={
                    },
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
            doctors = UserProfile.objects.filter(role="doctor").values('designation', 'user_id')

            designation_counts = {}

            for doctor in doctors:
                designation = doctor["designation"]
                if designation not in designation_counts:
                    designation_counts[designation] = {"daily": 0, "monthly": 0, "yearly": 0}

                # Count patients added under this doctor for today
                daily_count = PatientProfile.objects.filter(
                    user_id=doctor["user_id"], 
                    added_date__date=now().date()
                ).count()

                # Count patients added under this doctor for this month
                monthly_count = PatientProfile.objects.filter(
                    user_id=doctor["user_id"], 
                    added_date__month=now().month,
                    added_date__year=now().year
                ).count()

                # Count patients added under this doctor for this year
                yearly_count = PatientProfile.objects.filter(
                    user_id=doctor["user_id"], 
                    added_date__year=now().year
                ).count()

                # Update the designation counts
                designation_counts[designation]["daily"] += daily_count
                designation_counts[designation]["monthly"] += monthly_count
                designation_counts[designation]["yearly"] += yearly_count



            return Response(designation_counts, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)
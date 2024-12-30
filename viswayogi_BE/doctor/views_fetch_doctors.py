from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer
from user_profile.decorators import authenticate_user_session

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.TYPE_STRING),
}

class FetchDoctorsView(APIView):
    @swagger_auto_schema(
        operation_description="Fetch all doctors.",
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
                    description="Empty payload for fetching doctors",
                    properties={},
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
        auth_params = request.data.get('auth_params', {})
        user_id = auth_params.get('user_id')
        refresh_token = auth_params.get('refresh_token')

        # Validate auth_params
        if not user_id or not refresh_token:
            return Response(
                {"error": "Auth parameters are required (user_id and refresh_token)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Fetch all user profiles with the role "doctor"
            doctors = UserProfile.objects.filter(role="doctor")
            
            if not doctors.exists():
                return Response(
                    {"message": "No doctors found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            
            # Serialize the doctors data
            serializer = UserProfileSerializer(doctors, many=True)
            
            return Response(
                {"message": "Doctors fetched successfully", "doctors": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

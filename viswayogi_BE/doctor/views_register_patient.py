from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import PatientProfileSerializer
from user_profile.decorators import authenticate_user_session
from django.contrib.auth.hashers import make_password, check_password

HEADER_PARAMS = {
    'access_token': openapi.Parameter('accesstoken', openapi.IN_HEADER, description="local header param", type=openapi.IN_HEADER),
}

class PatientRegisterView(APIView):
    @swagger_auto_schema(
        operation_description="To register a patient.",
        manual_parameters=[HEADER_PARAMS['access_token']],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "auth_params": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="Authentication-related parameters (optional)",
                    properties={
                        "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="User ID"),
                        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Any other parameter"),
                    },
                ),
                "payload": openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    description="User registration details",
                    properties={
                        "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Full name of the user"),
                        "sex": openapi.Schema(type=openapi.TYPE_STRING, description="sex of patient"),
                        "dob": openapi.Schema(type=openapi.FORMAT_DATETIME, description="date of birth of patient"),
                        "health_info": openapi.Schema(type=openapi.TYPE_STRING, description="health information"),
                        "patient_phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number"),
                        "address": openapi.Schema(type=openapi.TYPE_STRING, description="address of the patient"),
                        "doctor_id":openapi.Schema(type=openapi.TYPE_STRING, description="doctor id"),
                    },
                ),
            },
            required=["auth_params","payload"],  # `payload` is required
        ),
        responses={
            201: openapi.Response(
                "User registered successfully",
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING, description="Success message"),
                        "user_data": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Serialized user data",
                            properties={
                                "user_id": openapi.Schema(type=openapi.TYPE_STRING, description="User ID"),
                                "full_name": openapi.Schema(type=openapi.TYPE_STRING, description="Full name"),
                                "email_id": openapi.Schema(type=openapi.TYPE_STRING, description="User email address"),
                                "patient_phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone number"),
                                "added_date": openapi.Schema(type=openapi.FORMAT_DATETIME, description="Creation date"),
                            },
                        ),
                    },
                ),
            ),
            400: "Validation errors",
        },
    )
    @authenticate_user_session
    def post(self, request):
        payload = request.data.get('payload', {})
        full_name = payload.get('full_name')
        phone_no = payload.get('patient_phone')
        address = payload.get('address')
        sex = payload.get('sex')
        dob = payload.get('dob')
        health_info = payload.get('health_info')
        user_id = payload.get('doctor_id')

        if not full_name:
            return Response(
                {"error": "Full name, email ID, and password are required in the payload."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

        serializer = PatientProfileSerializer(
            data={
                "full_name": full_name,
                "phone_no": phone_no,
                "address": address,
                "Sex": sex,
                "DOB": dob,
                "Health_info": health_info,
                "user_id":user_id
            }
        )
        if serializer.is_valid():
            user = serializer.save()

            user_data = {
                "full_name": full_name,
                "phone_no": phone_no,
                "address": address
            }

            return Response(
                {"message": "User registered successfully", "user_data": user_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
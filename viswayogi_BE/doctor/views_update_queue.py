from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Appointment
from .serializers import AppointmentSerializer
from user_profile.decorators import authenticate_user_session


class UpdateQueueView(APIView):
    """
    Updates an appointment and broadcasts the updated queue.
    """
    def post(self, request):

        payload = request.data.get('payload', {})
        appointment_id = payload.get('appointment_id')
        data = payload.get('data')
        try:
            appointment = Appointment.objects.get(appointment_id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # ✅ Fetch updated queue with correct sorting
            updated_queue = list(
                Appointment.objects.filter(done=False)
                .order_by(F("ready").desc(), "appointment_sch")  # ✅ Ready first, then sort by time
                .values()
            )

            # ✅ Send real-time update to WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "queue_updates",  # WebSocket group name
                {
                    "type": "send_queue_update",
                    "queue_data": updated_queue,
                },
            )

            return Response(
                {"message": "Appointment updated", "appointment": serializer.data},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.conf import settings
from openai.types.video_extend_params import Video
from rest_framework import generics
from .models import Events
from .serializers import EventsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .Camera import CameraController
from django.http import FileResponse, Http404
import os
from .views import camera


class EventsList(generics.ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer











# camera_app/api_views.py


@api_view(['POST'])
def start_recording(request):
    global recording, writer
    recording = True
    writer = cv2.VideoWriter(
        'output.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        20.0,
        (640, 480)
    )
    return JsonResponse({"status": "recording started"})

@api_view(['POST'])
def stop_recording(request):
    global recording, writer
    recording = False
    if writer:
        writer.release()
    return JsonResponse({"status": "recording stopped"})


@api_view(['GET'])
def list_recordings(request):
    files = [f for f in os.listdir('.') if f.endswith('.mp4')]
    return Response({"videos": files})


@api_view(['GET'])
def download_video(request, filename):
    file_path = os.path.join(settings.BASE_DIR, filename)

    if not os.path.exists(file_path):
        raise Http404("Video file not found")

    return FileResponse(open(file_path, 'rb'), as_attachment=True)




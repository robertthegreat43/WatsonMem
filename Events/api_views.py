from django.conf import settings
from rest_framework import generics
from .models import Events
from .serializers import EventsSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import FileResponse, Http404
import os
from .Camera import camera_controller




class EventsList(generics.ListAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


@api_view(['POST'])
def start_recording(request):
    filename = camera_controller.start_recording()
    return Response({"status": "recording started", "file": filename})


@api_view(['POST'])
def stop_recording(request):
    camera_controller.stop_recording()
    return Response({"status": "recording stopped"})


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




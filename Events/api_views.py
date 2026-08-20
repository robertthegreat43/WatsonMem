import os
import cv2
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import the recording variables from views.py
from .Camera import recording, writer, camera



@api_view(['POST'])
def start_recording(request):
    from .views import recording, writer  # ensure shared state

    recording = True
    writer = cv2.VideoWriter(
        'output.mp4',
        cv2.VideoWriter_fourcc(*'mp4v'),
        20.0,
        (640, 480)
    )

    # Update shared state in views.py
    from . import views
    views.recording = recording
    views.writer = writer

    return JsonResponse({"status": "recording started"})


@api_view(['POST'])
def stop_recording(request):
    from .views import recording, writer

    recording = False
    if writer:
        writer.release()

    # Update shared state
    from . import views
    views.recording = recording
    views.writer = None

    return JsonResponse({"status": "recording stopped"})


@api_view(['GET'])
def list_recordings(request):
    files = [f for f in os.listdir(settings.BASE_DIR) if f.endswith('.mp4')]
    return Response({"videos": files})


@api_view(['GET'])
def download_video(request, filename):
    file_path = os.path.join(settings.BASE_DIR, filename)

    if not os.path.exists(file_path):
        raise Http404("Video file not found")

    return FileResponse(open(file_path, 'rb'), as_attachment=True)

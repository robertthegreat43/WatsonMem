import os
import cv2
from django.conf import settings
from django.http import FileResponse, Http404, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Import the recording variables from views.py

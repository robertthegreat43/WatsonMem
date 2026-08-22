
from django.contrib import  auth
from django.urls import  include
from . import views, api_views
from django.urls import path
from .views import video_feed
from .api_views import start_recording, stop_recording, list_recordings, download_video






from django.contrib import auth
from django.urls import include
from . import views, api_views
from django.urls import path

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('items/', views.items_list, name="items_list"),
    path('accounts/profile/', views.profile, name='profile'),
    path('index/', views.index, name="index"),
    path('Videorecording/', views.video, name='videorecording'),
    path('daily_bread/',views.daily_bread,name='daily_bread'),
    path('prayers_for_those_in_need/',views.prayers_for_those_in_need,name='prayers_for_those_in_need'),
    path('logged_out/', views.logged_out, name='logout'),
    path("accounts/", include(("django.contrib.auth.urls", "auth"),namespace="accounts")),
    path("accounts/password_reset/done/",auth.views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    path("accounts/reset/done/", auth.views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
    path('api/all_events/', api_views.EventsList.as_view(), name="all_events"),
    path('video_feed/', views.video_feed, name='video_feed'),  # Added name parameter
    path('api/start_recording/', api_views.start_recording),
    path('api/stop_recording/', api_views.stop_recording),
    path('api/videos/', api_views.list_recordings),
    path('api/download/<str:filename>/', api_views.download_video, name='download_video'),
    path('api/biblechat/', views.biblechat_api, name='biblechat_api'),
    path('biblechat/', views.biblechat, name='biblechat'),
]




]

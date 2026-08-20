from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, auth
from django.urls import path, include
from . import views, api_views

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('items/', views.items_list, name="items_list"),
    path('accounts/profile/', views.profile, name='profile'),
    path('index/', views.index, name="index"),
    path('daily_bread/', views.daily_bread, name='daily_bread'),
    path('prayers_for_those_in_need/', views.prayers_for_those_in_need, name='prayers_for_those_in_need'),
    path('logged_out/', views.logged_out, name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/password_reset/done/", auth.views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/done/", auth.views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('api/biblechat/', views.biblechat_api, name='biblechat_api'),
    path('biblechat/', views.biblechat, name='biblechat'),
]

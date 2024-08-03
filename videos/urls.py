from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import RedirectView

from .views import CustomLoginView, video_dashboard, video_list, video_detail, like_video, vote_video, register, upload_video, verify_otp, resend_otp

urlpatterns = [

    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('video_dashboard/', video_dashboard, name='video_dashboard'),
    path('videos/', video_list, name='video_list'),
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('like/<int:video_id>/', like_video, name='like_video'),
    path('vote/<int:video_id>/', vote_video, name='vote_video'),
    path('register/', register, name='register'),
    path('upload/', upload_video, name='upload_video'),
    path('verify_otp/<int:user_id>/', verify_otp, name='verify_otp'),
    path('resend_otp/<int:user_id>/', resend_otp, name='resend_otp'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

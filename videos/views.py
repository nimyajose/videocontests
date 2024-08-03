# views.py
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Video, Like, View, Vote
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import RegistrationForm, OTPForm, VideoUploadForm
from .models import OTPVerification, UserProfile

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

@login_required
def video_dashboard(request):
    videos = Video.objects.filter(user=request.user)

    return render(request, 'video_dashboard.html', {'videos': videos})
def video_list(request):
    videos = Video.objects.all()
    return render(request, 'video_list.html', {'videos': videos})

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    View.objects.get_or_create(video=video)
    return render(request, 'video_detail.html', {'video': video})

@login_required
def like_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    Like.objects.get_or_create(user=request.user, video=video)
    return redirect('video_detail', video_id=video.id)

@login_required
def vote_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user = request.user

    if Vote.objects.filter(user=user, video=video).exists():
        messages.error(request, "You have already voted for this video.")
        return redirect('video_detail', video_id=video.id)

    Vote.objects.create(user=user, video=video)
    messages.success(request, "Thank you for voting!")
    return redirect('video_detail', video_id=video.id)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            otp_verification = OTPVerification.objects.create(user=user)
            otp_verification.generate_otp()
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp_verification.otp}',
                'from@example.com',
                [user.email],
            )
            return redirect('verify_otp', user_id=user.id)
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('video_dashboard')
    else:
        form = VideoUploadForm()
    return render(request, 'upload_video.html', {'form': form})

def verify_otp(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            otp_verification = OTPVerification.objects.filter(user=user, otp=otp).first()
            if otp_verification and otp_verification.is_valid():
                user.userprofile.is_verified = True
                user.userprofile.save()
                login(request, user)
                return redirect('video_list')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form, 'user': user})

def resend_otp(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    # Your OTP resending logic here
    messages.success(request, 'OTP has been resent.')
    return redirect('verify_otp', user_id=user.id)

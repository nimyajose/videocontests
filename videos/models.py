from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string

# In models.py
class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)  # Field for tracking views
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)  # ManyToManyField for likes

    def __str__(self):
        return self.title

    @property
    def views_count(self):
        return View.objects.filter(video=self).count()

    @property
    def likes_count(self):
        return Like.objects.filter(video=self).count()

    @property
    def liked_by_users(self):
        return User.objects.filter(like__video=self)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='likes_set', on_delete=models.CASCADE)  # Changed related_name
    liked_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = ('user', 'video')

class View(models.Model):
    video = models.ForeignKey(Video, related_name='views_set', on_delete=models.CASCADE)  # Changed related_name
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('video', 'viewed_at')

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)

class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        self.otp = ''.join(random.choices(string.digits, k=6))
        self.save()

    def is_valid(self):
        return (timezone.now() - self.created_at).seconds < 300  # OTP is valid for 5 minutes

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for djangogram.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F','Femaile'),
        ('C','Custom'),
    ]

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    user_name = models.CharField(blank=True,max_length=255)
    profile_photo = models.ImageField(blank=True)
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True) 
    email=models.CharField(blank=True,max_length=255)
    phone_number=models.CharField(blank=True, max_length=255)
    gender=models.CharField(blank=True, choices=GENDER_CHOICES, max_length=255)
    followers = models.ManyToManyField("self") #user 와 user가 다대다 관계이므로 self
    following = models.ManyToManyField("self")
    def get_absolute_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.username})

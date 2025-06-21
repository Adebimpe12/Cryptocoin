from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    gen = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    countries = [
        ("Nigeria", "Nigeria"),
        ("Ghana", "Ghana"),
        ("United Kingdom", "United Kingdom"),
        ("United Sates Of America", "United States Of America"),
    ]

    states = [
        ("Oyo", "Oyo"),
        ("Abia", "Abia"),
        ("Osun", "Osun"),
        ("Lagos", "Lagos"),
        ("Kano", "Kano"),
        ("Abuja", "Abuja"),
    ]

    position = [
        ("Chairman", "Chairman"),
        ("Director", "Director"),
        ("Supervisor", "Supervisor"),
        ("Admin", "Admin"),
        ("Delivery Agent", "Delivery Agent"),
        ("Store Keeper", "Store Keeper"),
    ] 

    ma_status = [
        ("Single", "Single"),
        ("Married", "Married"),
        ("Divorce", "Complicated"),
        ("Complicated", "Complicated"),
    ]


    profile_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, null=True, blank=True, unique=False)
    phone = models.CharField(max_length=11, null=True, blank=True, unique=False)
    date_of_birth = models.DateField(unique=False, max_length=11, null=True)
    gender = models.CharField(choices=gen, unique=False, max_length=11, null=True)
    nationality = models.CharField(choices=countries, unique=False, max_length=50, null=True)
    state = models.CharField(choices=states, unique=False, max_length=20, null=True) 
    means_of_identity = models.ImageField(upload_to='identityImage/', unique=False, null=True)
    particulars = models.FileField(upload_to='particularsImage/', unique=False, null=True)
    profile_passport = models.ImageField(upload_to='profileImage/', unique=False, null=True)
    position = models.CharField(choices=position, unique=False, max_length=25, null=True) 
    marital_status = models.CharField(choices=ma_status, unique=False, max_length=20, null=True) 
    staff = models.BooleanField(default=False, unique=False)
    next_of_kin = models.CharField(unique=False, max_length=20, null=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
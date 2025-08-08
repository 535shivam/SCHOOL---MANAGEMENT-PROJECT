# accounts/signals.py

from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, StudentInfoModel, TeacherInfoModel

# Create profile when user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance, role='student')  # Default role


# Delete related models when user is deleted
@receiver(post_delete, sender=User)
def delete_related_models(sender, instance, **kwargs):
    print(f"🧹 Deleting related models for user: {instance.username}")

    try:
        instance.profile.delete()
    except Profile.DoesNotExist:
        print("No profile found")

    try:
        instance.studentinfomodel.delete()
    except StudentInfoModel.DoesNotExist:
        print("No student info found")

    try:
        instance.teacherinfomodel.delete()
    except TeacherInfoModel.DoesNotExist:
        print("No teacher info found")

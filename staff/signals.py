# Disabled — user creation handled by StaffCreateForm
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import StaffProfile
#
# User = get_user_model()
#
# @receiver(post_save, sender=StaffProfile)
# def auto_create_user(sender, instance, created, **kwargs):
#     if created and not instance.user:
#         username = instance.name.lower().replace(' ', '_')[:150]
#         base = username
#         suffix = 1
#         while User.objects.filter(username=username).exists():
#             username = f'{base}_{suffix}'
#             suffix += 1
#         user = User.objects.create_user(
#             username=username,
#             email=instance.email,
#             first_name=instance.name,
#             password='staff123',
#         )
#         instance.user = user
#         instance.save(update_fields=['user'])

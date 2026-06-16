from notifications.tasks import send_welcome_email as send_welcome_email_task
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import NewUser

@receiver(post_save, sender=NewUser)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email_task.delay(instance.id)
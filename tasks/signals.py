
# from .models import Task
# from notifications.models import Notification
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer


# @receiver(post_save, sender=Task)
# def task_created_notification(sender,instance,created,**kwargs):

#     if created:
#         recipents=[instance.created_by]

#         if instance.assigned_to and instance.assigned_to != instance.created_by:
#             recipents.append(instance.assigned_to)

#         for user in recipents:

#                 Notification.objects.create(
#                 user=user,
#                 title="Task Created",
#                 message=f"Task '{instance.title}' has been created."

#             )    
#                 channel_layer = get_channel_layer()
#                 async_to_sync(channel_layer.group_send)(
#                 f"user_{user.id}",
#                 {
#                     "type": "user_notification",
#                     "title": "New Task Created",
#                     "message": f'Task "{instance.title}" has been created.'
#                 }
#         )


# Signals for task


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.models import Notification
from tasks.models import Task
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Task)
def task_created_notification(sender, instance, created, **kwargs):
    if created:
       
        recipients = [instance.created_by]
        if instance.assigned_to and instance.assigned_to != instance.created_by:
            recipients.append(instance.assigned_to)

        for user in recipients:
            Notification.objects.create(
                user=user,
                title=f"Task Created: {instance.title}",
                message=f'Task "{instance.title}" has been created.'
            )
            channel_layer = get_channel_layer()
            print("SENDING TO GROUP:", f"user_{user.id}")
            async_to_sync(channel_layer.group_send)(
                  f"user_{user.id}",
                {
                    "type": "user_notification",
                    "title": f"New Task Created: {instance.title}",
                    "message": f'Task "{instance.title}" has been created.'
                }
            )
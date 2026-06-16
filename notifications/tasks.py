from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def send_welcome_email(user_id):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    # Here you would implement the logic to send an email to the user
    print("=" * 50)
    print(f"Welcome email sent to {user.email}")
    print(f"Hello {user.user_name}, welcome to our platform!")
    print("=" * 50)


    return f"Welcome email sent to {user.email}"

@shared_task
def count_users():
    User = get_user_model()

    total_users = User.objects.count()

    print("=" * 50)
    print(f"TOTAL USERS: {total_users}")
    print("=" * 50)

    return total_users
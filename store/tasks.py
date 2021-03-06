from django.core.mail import EmailMessage
from decouple import config
from celery import shared_task


@shared_task(bind=True, queue='email_queue')
def send_mail(self, email_id, file_path, store_type):
    email = EmailMessage(
        subject=f'{store_type} data from Store Finder',
        body="Thank you for using our service",
        from_email=config('EMAIL_HOST_USER'),
        to=[email_id, ],
    )
    email.attach_file(file_path, 'text/csv')
    email.send(fail_silently=False)
    return 'Mail Sent'

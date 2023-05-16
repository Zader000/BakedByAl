from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import smtplib
import ssl
from email.mime.text import MIMEText


@receiver(post_save, sender=Order)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL('mail.zbiggs.com', 465, context=context)
        server.set_debuglevel(1)
        server.login("noreply@zbiggs.com", 'z{E3Nl+.EUUl')
        msg = MIMEText(f"Thank you for your order, {instance.name}! Your order number is {instance.id}.")
        msg['Subject'] = 'Baked By Al Order Received'
        msg['From'] = 'noreply@zbiggs.com'
        msg['To'] = instance.email

        server.sendmail("noreply@zbiggs.com", instance.email, msg.as_string())
        server.quit()

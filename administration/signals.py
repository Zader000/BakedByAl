from django.db.models.signals import pre_save
from django.dispatch import receiver
from BakedByAl.models import Order
import smtplib
import ssl
from email.mime.text import MIMEText

@receiver(pre_save, sender=Order)
def send_status_change_email(sender, instance, **kwargs):
    try:
        old_order = Order.objects.get(pk=instance.id)
        if old_order.order_status != instance.order_status:
            if instance.order_status == 'C':
                new_status = 'Confirmed'
            elif instance.order_status == 'P':
                new_status = 'Pending'
            elif instance.order_status == 'F':
                new_status = 'Fulfilled'
            elif instance.order_status == 'X':
                new_status = 'Cancelled'
            else:
                new_status = 'Unknown'
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL('mail.zbiggs.com', 465, context=context)
            server.set_debuglevel(1)
            server.login("noreply@zbiggs.com", 'z{E3Nl+.EUUl')
            msg = MIMEText(f"Your order status has been updated to {new_status}.")
            msg['Subject'] = 'Baked By Al Order Status Update'
            msg['From'] = 'noreply@zbiggs.com'
            msg['To'] = instance.email

            server.sendmail("noreply@zbiggs.com", instance.email, msg.as_string())
            server.quit()
    except Order.DoesNotExist:
        pass
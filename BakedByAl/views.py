import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib import messages
import smtplib
import ssl
from email.mime.text import MIMEText

from BakedByAl.models import GalleryItem, Order, OrderItem


# Create your views here.


def index(request):
    return render(request, 'BakedByAl/index.html')


def about(request):
    return render(request, 'BakedByAl/about.html')


def contact(request):
    if request.method == 'POST' and request.POST.get('name') is not None:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        try:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL('mail.zbiggs.com', 465, context=context)
            server.set_debuglevel(1)
            server.login("noreply@zbiggs.com", 'z{E3Nl+.EUUl')
            msg = MIMEText(f"Message from {name} ({email}):\n\n{message}")
            msg['Subject'] = 'Baked By Al Order Received'
            msg['From'] = 'noreply@zbiggs.com'
            msg['To'] = 'zach@zbiggs.com'
            server.sendmail("noreply@zbiggs.com", "zach@zbiggs.com", msg.as_string())
            server.quit()
            messages.success(request, 'Message sent successfully!')
        except smtplib.SMTPException as e:
            messages.error(request, 'Error sending email')
    return render(request, 'BakedByAl/contact.html')

def gallery(request):
    all_items = GalleryItem.objects.all()
    search = request.GET.get('search')
    is_search = False
    if search != '' and search is not None:
        all_items = all_items.filter(name__icontains=search)
        is_search = True

    paginator = Paginator(all_items, 3)
    page_number = request.GET.get('page')
    cakes = paginator.get_page(page_number)
    return render(request, 'BakedByAl/gallery.html', {'cakes': cakes, 'is_search': is_search})


def cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
        request.session.modified = True
    if request.method == 'POST' and request.POST.get('cake_id') is not None:
        if request.POST.get('cake_id') not in request.session['cart']:
            request.session['cart'].append(request.POST.get('cake_id'))
            request.session.modified = True
    elif request.method == 'GET' and request.GET.get('remove') is not None:
        request.session['cart'].remove(request.GET.get('remove'))
        request.session.modified = True

    cart = []
    for id in request.session['cart']:
        cart.append(GalleryItem.objects.get(id=id))

    return render(request, 'BakedByAl/cart.html', {'cart': cart})


def order_confirmation(request):
    if request.method == 'POST':
        order = Order()
        order.name = request.POST.get('name')
        order.email = request.POST.get('email')
        order.phone = request.POST.get('phone')
        order.date = datetime.datetime.now()
        order.save()
        order_lines = []
        messages.success(request, f'Order placed successfully!')
        for item in request.session['cart']:
            oi = OrderItem(product=GalleryItem.objects.get(id=item), quantity=request.POST.get(f'item-qty{item}'),
                           order=order)
            oi.save()
            order_lines.append(oi)
        order.save()
        request.session['cart'] = []
        request.session.modified = True
    return render(request, 'BakedByAl/order-confirmation.html')
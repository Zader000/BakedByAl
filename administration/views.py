from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import GalleryItemForm, OrderForm
from BakedByAl.models import Order, OrderItem, GalleryItem


# Create your views here.


@login_required
def index(request):
    return render(request, 'administration/index.html')


@login_required
def order_delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == "GET" and request.GET.get('confirmed') == 'true':
        order.delete()
        return redirect('administration:orders')
    return render(request, 'administration/order_delete.html', {'order': order})


@login_required
def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('administration:order_detail', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'administration/order_create.html', {'form': form})


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)

    if request.method == "POST" and request.POST.get('order_status') is not None:
        order.order_status = request.POST.get('order_status')
        order.save()

    if request.method == "POST" and request.POST.get('item_id') is not None:
        oi = OrderItem.objects.create(
            order=order,
            product=GalleryItem.objects.get(pk=request.POST.get('item_id')),
            quantity=request.POST.get('quantity'))
        oi.save()

    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'administration/order_detail.html', context)


@login_required
def orders(request):
    pending_orders = Order.objects.filter(order_status='P').order_by('date')
    confirmed_orders = Order.objects.filter(order_status='C').order_by('date')
    cancelled_orders = Order.objects.filter(order_status='X').order_by('date')
    fulfilled_orders = Order.objects.filter(order_status='F').order_by('date')

    context = {
        'pending_orders': pending_orders,
        'confirmed_orders': confirmed_orders,
        'cancelled_orders': cancelled_orders,
        'fulfilled_orders': fulfilled_orders
    }
    # get order items

    return render(request, 'administration/orders.html', context)


@login_required
def order_item_edit(request, order_item_id):
    return render(request, 'administration/order-item-edit.html')


@login_required
def order_item_delete(request, order_item_id):
    order_item = OrderItem.objects.get(pk=order_item_id)
    if request.method == "GET" and request.GET.get('confirmed') == 'true':
        order_item.delete()
        return redirect('administration:order_detail', order_id=order_item.order.id)
    return render(request, 'administration/order-item-delete.html')


@login_required
def order_item_create(request, order_id):
    items = GalleryItem.objects.all()
    context = {
        'items': items,
        'order_id': order_id
    }
    return render(request, 'administration/order-item-create.html', context)


@login_required
def gallery_items(request):
    all_items = GalleryItem.objects.all()
    paginator = Paginator(all_items, 10)
    page_number = request.GET.get('page')
    items = paginator.get_page(page_number)
    context = {
        'items': items
    }
    return render(request, 'administration/gallery-items.html', context)


@login_required
def gallery_item_create(request):
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('administration:gallery_items')
    form = GalleryItemForm()
    return render(request, 'administration/gallery-item-create.html', {'form': form})


@login_required
def gallery_item_edit(request, gallery_item_id):
    item = GalleryItem.objects.get(pk=gallery_item_id)
    if request.method == "POST":
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        item.save()
        return redirect('administration:gallery_items')
    return render(request, 'administration/gallery-item-edit.html', {'item': item})


@login_required
def gallery_item_delete(request, gallery_item_id):
    item = GalleryItem.objects.get(pk=gallery_item_id)
    if request.method == "GET" and request.GET.get('confirmed') == 'true':
        item.delete()
        return redirect('administration:gallery_items')
    return render(request, 'administration/gallery-item-delete.html', {'item': item})


@login_required
def gallery_item_detail(request, gallery_item_id):
    item = GalleryItem.objects.get(pk=gallery_item_id)
    context = {
        'item': item
    }
    return render(request, 'administration/gallery-item-detail.html', context)
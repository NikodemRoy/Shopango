from django.shortcuts import redirect, render
from django.http import HttpResponse

from APPS.orders.models import Order, OrderProduct, Payment
from APPS.store.models import Product

from .forms import OrderForm
import datetime
from APPS.cart.models import Cart, CartItem

from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import json
# Create your views here.


def payment(request):
    client_order = json.loads(request.body)
    print(client_order)
    
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=client_order['orderID'])

    payment = Payment(
        user = request.user,
        payment_id = client_order['transID'],
        payment_method = client_order['payment_method'],
        amount_paid = order.order_total,
        status = client_order['status']
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    

    # moving cart items to Order Product table

    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_var = cart_item.variations.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variations.set(product_var)
        order_product.save()
        
        # reducing the quantity after sale
        product = Product.objects.get(id=item.product_id)
        product.stock -= item.quantity
        product.save()
    
    # clearing cart
    CartItem.objects.filter(user=request.user).delete()

    # sending order confirmation email
    user = request.user
    mail_subject = 'Thanks for your order!'
    message = render_to_string('accounts/order_confirmation_email.html', {
        'user': user,
        'order':order
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()



    # for item in cart_items:
    #     order = order.id
    #     payment = payment
    #     user = request.user.id
    #     product = item.product_id
    #     quantity = item.quantity
    #     product_price = item.product.price
    #     ordered = True
    #     OrderProduct.objects.create(order = order, payment = payment, user = user, product = product,
    #      quantity = quantity, product_price = product_price, ordered = ordered)



    return render(request, 'orders/payment.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round(0.19 * total, 2)
    grand_total = total

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            order_note = form.cleaned_data['order_note']
            order_total = grand_total

            order = Order.objects.create(first_name=first_name, last_name=last_name, phone=phone, email=email,
                                         address_line_1=address_line_1, address_line_2=address_line_2,
                                         country=country, state=state, city=city, order_note=order_note, order_total=grand_total, tax=tax)
            form.save(commit=False)

            ip = request.META.get('REMOTE_ADDR')
            # generate order number:
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # 20210305
            order_number = current_date + str(order.id)

            order.ip = ip
            order.order_number = order_number
            order.user = current_user
            order.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }
            return render(request, 'orders/payment.html', context)
    else:
        return redirect('store')


# def place_order(request, total=0, quantity=0):
#     current_user = request.user

#     cart_items = CartItem.objects.filter(user=current_user)
#     if cart_items.count() <= 0:
#         return redirect('store')

#     grand_total= 0
#     tax = 0

#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity )
#         quantity += cart_item.quantity
#     tax = 0.19 * total
#     grand_total = total

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Store all the billing information inside Order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             # Generate order number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime("%Y%m%d") #20210305
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()

#             return redirect('checkout')
#     else:
#         return redirect('store')


# def place_order(request, total=0, quantity=0):
#     current_user = request.user

#     cart_items = CartItem.objects.filter(user=current_user)
#     if cart_items.count() <= 0:
#         return redirect('store')

#     grand_total= 0
#     tax = 0

#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity )
#         quantity += cart_item.quantity
#     tax = 0.19 * total
#     grand_total = total

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = Order()
#             order.user = current_user
#             order.first_name = form.cleaned_data['first_name']
#             order.last_name = form.cleaned_data['last_name']
#             order.phone = form.cleaned_data['phone']
#             order.email = form.cleaned_data['email']
#             order.address_line_1 = form.cleaned_data['address_line_1']
#             order.address_line_2 = form.cleaned_data['address_line_2']
#             order.country = form.cleaned_data['country']
#             order.state = form.cleaned_data['state']
#             order.city = form.cleaned_data['city']
#             order.order_note = form.cleaned_data['order_note']
#             order_total = grand_total
#             tax = tax
#             ip = request.META.get('REMOTE_ADDR')
#             order.save(commit=False)

#                 #generate order number:
        # year = int(datetime.date.today().strftime('%Y'))
        # day = int(datetime.date.today().strftime('%d'))
        # month = int(datetime.date.today().strftime('%m'))
        # d = datetime.date(day, month, year)
        # current_date = d.strftime("%d%m%Y")
#             order_number = current_date + str(form.id)
#             order.order_number = order_number
#             order.save()
#             return redirect('checkout')
#     else:
#         return redirect('store')

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core import mail
from matlyuba import settings




@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})




def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            email_subject = 'MATLYUBA :: Новая заявка с сайта '
            email_body = "С сайта отправлено новое сообщение\n\n" \
                         "Размеры: %s \n" \
                         "Имя: %s \n" \
                         "Фамилия: \n" \
                         "Email: %s\n" \
                         "Адрес: %s\n" \
                         "Телефон: %s\n"\
                          "Город: %s\n" \
                         "%s " % \
                         (form.cleaned_data['size'], form.cleaned_data['first_name'],  form.cleaned_data['last_name'], form.cleaned_data['email'],form.cleaned_data['address'],form.cleaned_data['postal_code'], form.cleaned_data['city'])
            # address = request.POST.get("address")
            send_mail(email_subject, email_body,  settings.EMAIL_HOST_USER, ['momyn97.mu@gmail.com'],)

            order = form.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()

            return render(request, 'cart/created.html',
                          {'order': order })
    else:
        form = OrderCreateForm
    return render(request, 'cart/create.html',
                  {'cart': cart, 'form': form})

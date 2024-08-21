from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from shop.models import Product
from .forms import CartAddProductForm
from .cart import Cart
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender
# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'],
                 override_quantity=cd['override'])

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for itam in cart:
        itam['update_quantity_form'] =\
            CartAddProductForm(initial={'quantity': itam['quantity'],
                                        'override': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if (cart_products):
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4)
    else:
        recommended_products = []
    return render(request, 'cart/detail.html',
                  {'cart': cart, 'coupon_apply_form':coupon_apply_form, 'recommended_products': recommended_products})
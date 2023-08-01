from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect

from artGalleryMain.Validation.FormValidation import CheckOutValidation
from artGalleryMain.Validation.UserValidation import checkUserPermission
from artGalleryMain.models import *


# Create your views here.
@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def cart(request):
    cart = Cart.getOrCreateCartByUser(request.user)
    if cart.getCartItems().count() == 0:
        return render(request, "main/cartIsEmpty.html")
    return render(request, 'main/cart.html', {
        'cart': cart
    })


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def checkout(request):
    cart = Cart.getOrCreateCartByUser(request.user)
    if cart.getCartItems().count() == 0:
        return render(request, "main/cartIsEmpty.html")
    if request.method == "POST":
        errors, address = CheckOutValidation(request.POST)
        if len(errors) > 0:
            for error in errors:
                messages.error(request, error)
            return render(request, 'main/checkout.html')
        cart.is_ordered = True
        address.save()
        cart.address = address
        cart.save()
        return redirect("/")
    return render(request, 'main/checkout.html')

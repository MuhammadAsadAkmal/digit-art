from django import template
from ..models import *
from ..artConfig import ART_TYPE
import re as regex

register = template.Library()


@register.filter(name="getCartItemCount")
def getListofCartItem(user):
    if user.is_authenticated:
        cart = Cart.getOrCreateCartByUser(user)
        return cart.getCartItems()[:2]
    return []


@register.filter(name="cart")
def getCart(user):
    if user.is_authenticated:
        cart = Cart.getOrCreateCartByUser(user)
        return cart
    return None
@register.filter(name="wistCount")
def wishCount(user):
    if user.is_authenticated:
        count = wishList.objects.filter(user=user).count()
        return count
    return None
@register.filter(name="getWishListItem")
def getWishListItem(user):
    if user.is_authenticated:
        count = wishList.objects.filter(user=user)[:3]
        return count
    return None


@register.filter(name="Cartcount")
def getCartCount(user):
    if user.is_authenticated:
        cart = Cart.getOrCreateCartByUser(user)
        return cart.getCartItems().count()
    return 0


isWishList = False


@register.simple_tag
def call_method(obj, method_name, *args):
    global isWishList
    method = getattr(obj, method_name)
    isWishList = method(*args)


@register.filter(name="isWishListed")
def isWishListed(user,*args):
    global isWishList
    return isWishList


@register.filter(name="category")
def getCategory(a, *args):
    art_type1 = list(ART_TYPE)
    art_type1.reverse()
    art_type1.append(["All", "All"])
    art_type1.reverse()
    # a = /store?sortBy=name&category=DEGITIAL_ART
    # getting data from url using regex
    a = regex.findall(r'category=(\w+)', a)
    if len(a) > 0:
        a = a[0]
    else:
        a = "All"
    art_type = []
    for i in art_type1:
        i = list(i)
        if i[0] == a:
            i.append(True)
        else:
            i.append(False)
        art_type.append(i)

    return art_type

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ..Validation.UserValidation import checkUserPermission
from ..models import *


# Create your views here.


def index(request):
    trending = Art.objects.filter(Q(cartitem__isnull=True) | Q(cartitem__cart__status=Cart.CANCELED)).distinct()[:8]
    # geeting random art from database
    randomArt = Art.objects.filter(
        Q(cartitem__isnull=True) | Q(cartitem__cart__status=Cart.CANCELED)).distinct().order_by("?")[:10]
    poster = HomePagePoster.objects.filter(isLastItem=False).order_by("-created_at").first()
    allPosters = HomePagePoster.objects.filter(isLastItem=False).order_by("-created_at")[1:3]
    lastItem = HomePagePoster.objects.filter(isLastItem=True).order_by("-created_at").first()

    return render(request, "main/index.html", {
        "cat": True,
        "trending": trending,
        "poster": poster,
        "allPosters": allPosters,
        "lastItem": lastItem,
        "randomArt": randomArt,
    })


def productDetail(request, title):
    try:
        art = Art.objects.get(title=title)
    except Art.DoesNotExist:
        return render(request, "main/404.html")

    return render(request, "main/productdetail.html", {
        "art": art
    })


def addToCart(request, title):
    if not request.user.is_authenticated or not request.user.is_active:
        return JsonResponse({"status": "error", "message": "User not logged in"}, status=401)
    if request.user.roles != USER:
        return JsonResponse({"status": "error", "message": "User not allowed"}, status=401)
    try:
        art = Art.objects.get(title=title)
        if CartItem.checkIfItemIsInCart(art):
            if CartItem.checkIfUserHaveThatArtInCart(art, request.user):
                return JsonResponse({"status": "error", "message": "Art already in cart"})
            return JsonResponse({"status": "error", "message": "Art Not available"})
        CartItem.addItemToTheCart(art, request.user)
        return JsonResponse({"status": "success", "message": "Art added to cart"})
    except Art.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Art not found"})


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def removeItem(request, idItem):
    try:
        a = CartItem.objects.get(id=idItem)
        a.delete()
        return redirect("cart")
    except CartItem.DoesNotExist:
        return redirect("cart")


def pageNotFound(request):
    return render(request, "main/404.html")
def chatbot(request):
    return render(request, "main/chatbot.html")


def store(request):
    itemCount = 9 if request.GET.get("itemCount") is None else int(request.GET.get("itemCount"))
    page = 1 if request.GET.get("page") is None else int(request.GET.get("page"))
    sortBy = "name" if request.GET.get("sortBy") is None else request.GET.get("sortBy")
    category = "All" if request.GET.get("category") is None else request.GET.get("category")
    search = "" if request.GET.get("search") is None else request.GET.get("search")
    # getting all the arts that are not in cartItem table plus which are not sold using reverse relationship
    if category == "All":
        arts = Art.objects.all()
    else:
        arts = Art.objects.filter(category=category)
    if search != "":
        arts = arts.filter(Q(title__icontains=search) | Q(description__icontains=search))
    arts = arts.filter(Q(cartitem__isnull=True) | Q(cartitem__cart__status=Cart.CANCELED)).distinct()
    if sortBy == "name":
        arts = arts.order_by("title")
    elif sortBy == "price":
        arts = arts.order_by("price")
    elif sortBy == "date":
        arts = arts.order_by("created_at")
    # pagination
    arts = arts[(page - 1) * itemCount:page * itemCount]
    categories = list(ART_TYPE)
    categories.reverse()
    categories.append(("All", "All"))
    categories.reverse()
    return render(request, "main/store.html", {
        "arts": arts,
        "categories": categories,
        "selectedCategory": category,
        "sortBy": SORT_BY,
        "itemCount": ITEM_COUNT,
        "selectedSortBy": sortBy,
        "selectedItemCount": itemCount,
        "search": search,
    })


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def addToWishList(request, title):
    try:
        art = Art.objects.get(title=title)
        item = wishList.checkIfItemIsInWishList(art, request.user)
        if item.exists():
            item[0].delete()
        else:
            a = wishList(user=request.user, art=art)
            a.save()
        return redirect(request.META['HTTP_REFERER'])
    except Art.DoesNotExist:
        print("here 11")
        return redirect("pageNotFound")


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def wishlist(request):
    wishListItems = wishList.objects.filter(user=request.user)
    return render(request, "main/wishlist.html", {
        "wishListItems": [item.art for item in wishListItems]
    })


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def orders(request):
    orders = Cart.objects.filter(user=request.user, is_ordered=True).order_by("-created_at")
    return render(request, "main/myOrders.html", {
        "orders": orders
    })

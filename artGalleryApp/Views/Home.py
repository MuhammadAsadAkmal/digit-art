from time import sleep

from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from CustomTokens.UserToken import UserAuthenticationToken
from adminArtist.Serializers.UserSerializer import UserSerializer
from artGalleryApp.Searlizers.AddressSearlizer import AddressSerializer
from artGalleryApp.Searlizers.HomePagePosterSearlizer import HomePagePosterSerializer
from artGalleryApp.Searlizers import *
from artGalleryMain.models import *


@api_view(['GET'])
def getPoster(request):
    poster = HomePagePoster.objects.filter(isLastItem=False).order_by("-created_at").first()
    return JsonResponse(HomePagePosterSerializer(poster).data, status=status.HTTP_200_OK)


class store(generics.ListAPIView):
    authentication_classes = [UserAuthenticationToken]
    permission_classes = [IsAuthenticated]
    serializer_class = ArtSerializer

    def get_queryset(self):
        search = self.request.query_params.get('query') if self.request.query_params.get('query') else ""
        arts = Art.objects.all()
        arts = arts.filter(Q(title__icontains=search) | Q(description__icontains=search))
        arts = arts.filter(Q(cartitem__isnull=True) | Q(cartitem__cart__status=Cart.CANCELED)).distinct()
        arts = arts.order_by("-created_at")
        return arts


@api_view(['GET'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def getTrendingItem(request):
    trending = Art.objects.filter(Q(cartitem__isnull=True) | Q(cartitem__cart__status=Cart.CANCELED)).distinct()[:8]
    return JsonResponse({
        "data": ArtSerializer(trending, context={'user': request.user}, many=True).data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def placeOrder(request):
    cart = Cart.getOrCreateCartByUser(request.user)
    cartItems = CartItem.objects.filter(cart=cart)
    if not cartItems.exists():
        return JsonResponse({
            "type": 100,
            "success": False,
            "message": "cart is empty"
        }, status=status.HTTP_200_OK)
    address = request.data
    addresSearlizer = AddressSerializer(data=address)
    if not addresSearlizer.is_valid():
        return JsonResponse({
            "status": 104,
            "message": addresSearlizer.errors
        }, status=status.HTTP_200_OK)
    address = addresSearlizer.save()
    cart.address = address
    cart.is_ordered = True
    cart.save()
    return JsonResponse({
        "status": 200,
        "message": "order placed successfully"
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def getBaseData(request):
    cart = Cart.getOrCreateCartByUser(request.user)
    cartTemCount = CartItem.objects.filter(cart=cart).count()
    favCount = wishList.objects.filter(user=request.user).count()
    return JsonResponse({
        "cartTemCount": cartTemCount,
        "favCount": favCount
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def getOrderHistory(request):
    cart = Cart.objects.filter(user=request.user, is_ordered=True)
    orders = []
    for order in cart:
        orders.append({
            "OrderId": order.id,
            "items": CartItem.objects.filter(cart=order).count(),
            "title": CartItem.objects.filter(cart=order).first().art.title if CartItem.objects.filter(cart=order).first() else None,
            "total": order.getTotalPrice(),
            "OrderStatus": order.status,
            "date": order.orderDate.strftime("%b %d %Y") if order.orderDate else order.created_at,
            "image": CartItem.objects.filter(cart=order).first().art.image.url if CartItem.objects.filter(cart=order).first() else None
        })
    return JsonResponse({
        "orders": orders
    }, status=status.HTTP_200_OK)


@api_view(['POST', 'GET', 'DELETE'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def addToCart(request):
    if request.method == "DELETE":
        id = request.data.get("id")
        if not id:
            return JsonResponse({
                "type": "error",
                "message": "id is required"
            }, status=status.HTTP_200_OK)
        cartItem = CartItem.objects.filter(id=id)
        if not cartItem.exists():
            return JsonResponse({
                "type": "error",
                "message": "cartItem not found"
            }, status=status.HTTP_200_OK)
        cartItem.delete()
        return JsonResponse({
            "type": "success",
            "success": True,
            "message": "cartItem deleted successfully"
        }, status=status.HTTP_200_OK)
    if request.method == "GET":
        cart = Cart.getOrCreateCartByUser(request.user)
        cartItems = CartItem.objects.filter(cart=cart)
        return JsonResponse({
            "type": "success",
            "success": True,
            "data": CartItemSerializer(cartItems, many=True).data
        }, status=status.HTTP_200_OK)

    if "artId" not in request.data:
        return JsonResponse({
            "type": "error",
            "error": "artId is required"
        }, status=status.HTTP_200_OK)
    try:
        art = Art.objects.get(id=request.data.get("artId"))
        cart = Cart.getOrCreateCartByUser(request.user)
        cartItem = CartItem.objects.filter(cart=cart, art=art)
        if not cartItem.exists():
            CartItem.objects.create(cart=cart, art=art)
        return JsonResponse({
            "type": "success",
            "message": "Item added to cart",
            "cartCount": CartItem.objects.filter(cart=cart).count()
        }, status=status.HTTP_200_OK)
    except Art.DoesNotExist:
        return JsonResponse({
            "type": "error",
            "error": "Art not found"
        }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([UserAuthenticationToken])
@permission_classes([IsAuthenticated])
def favorite(request):
    if request.method == "POST":
        try:
            art = Art.objects.get(id=request.data.get("artId"))
            wish = wishList.objects.filter(user=request.user, art=art)
            if wish.exists():
                wish.delete()
                return JsonResponse({
                    "message": "success",
                    "type": "delete",
                    "count": wishList.objects.filter(user=request.user).count()
                }, status=status.HTTP_200_OK)
            wishList.objects.create(user=request.user, art=art)
            return JsonResponse({
                "message": "success",
                "type": "added",
                "count": wishList.objects.filter(user=request.user).count()

            }, status=status.HTTP_200_OK)

        except Art.DoesNotExist:
            return JsonResponse({
                "message": "error"
            }, status=status.HTTP_404_NOT_FOUND)

    arts = [wish.art for wish in wishList.getAllWishListItems(request.user)]
    return JsonResponse({
        "data": ArtSerializer(arts, many=True, context={
            'user': request.user
        }).data
    }, status=status.HTTP_200_OK)

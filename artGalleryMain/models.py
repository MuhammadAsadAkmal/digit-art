from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from artGalleryMain.managers import CustomUserManager
from .roles import *
from .artConfig import *


# Create your models here.
class ArtGalleryUsers(AbstractUser):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other")
    )
    first_name = None
    last_name = None
    username = models.CharField(max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    roles = models.CharField(max_length=100, null=False, blank=False, choices=ROLES, default=USER)
    dp = models.ImageField(upload_to="dp", null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, null=False, blank=False)
    REQUIRED_FIELDS = ["roles", "email"]
    objects = CustomUserManager()

    class Meta:
        abstract = False

    def isUserSuperAdmin(self):
        return self.roles == SUPER_ADMIN

    def isArtistOrAdmin(self):
        return self.roles == SUPER_ADMIN or self.roles == ARTIST

    def isNormalUser(self):
        return self.roles == USER

    def __str__(self):
        return self.email


class Art(models.Model):
    image = models.ImageField(upload_to="art", null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    price = models.FloatField(null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    artist = models.ForeignKey(ArtGalleryUsers, on_delete=models.CASCADE, null=False, blank=False)
    style = models.CharField(max_length=100, null=False, blank=False, choices=STYLE)
    medium = models.CharField(max_length=100, null=False, blank=False, choices=MEDIUM)
    subject = models.CharField(max_length=100, null=False, blank=False, choices=SUBJECT)
    category = models.CharField(max_length=100, null=False, blank=False, choices=ART_TYPE)
    shipping_fee = models.FloatField(null=False, blank=False, default=10.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getStyleValue(self):
        for i in STYLE:
            if i[0] == self.style:
                return i[1]

    def getMediumValue(self):
        for i in MEDIUM:
            if i[0] == self.medium:
                return i[1]

    def getSubjectValue(self):
        for i in SUBJECT:
            if i[0] == self.subject:
                return i[1]

    def getCategoryValue(self):
        for i in ART_TYPE:
            if i[0] == self.category:
                return i[1]

    def getTotalPrice(self):
        return self.price + self.shipping_fee

    def getPointList(self):
        return [self.getCategoryValue(), self.getStyleValue(), self.getMediumValue(), self.getSubjectValue()]

    def getShortDescription(self):
        return self.description[:100]

    def checkIfItemInWishList(self, user):
        return wishList.objects.filter(Q(user=user) & Q(art=self)).exists()

    def __str__(self):
        return self.title


class HomePagePoster(models.Model):
    image = models.ImageField(upload_to="homePagePoster", null=False, blank=False)
    subTitle = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    isLastItem = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.subTitle}"


class Address(models.Model):
    address1 = models.CharField(max_length=300, null=False, blank=False)
    address2 = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=100, null=False, blank=False)
    postal_code = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.address1}, {self.address2}, {self.city}, {self.country}, {self.postal_code}"


class Cart(models.Model):
    DELIVERED = "DELIVERED"
    CANCELED = "CANCELED"
    PENDING = "PENDING"
    ORDER_STATUS = (
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
        (PENDING, "Pending")
    )
    user = models.ForeignKey(ArtGalleryUsers, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, null=False, blank=False, choices=ORDER_STATUS, default=PENDING)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    orderDate = models.DateTimeField(null=True, blank=True)
    deliveryDate = models.DateTimeField(null=True, blank=True)

    def getOrderDate(self):
        if self.orderDate is None:
            return "Not Ordered"
        return self.orderDate.strftime("%d %b %Y")

    def getDeliveryDate(self):
        if self.deliveryDate is None:
            return "Not Delivered yet your order is in process"
        return self.deliveryDate.strftime("%d %b %Y")

    def save(self, *args, **kwargs):
        if self.is_ordered:
            self.orderDate = datetime.now()
        if self.status == self.DELIVERED:
            self.deliveryDate = datetime.now()
        super(Cart, self).save(*args, **kwargs)

    def getOrderAtDate(self):
        return self.created_at.strftime("%d %b %Y")

    def getStatusValue(self):
        for i in self.ORDER_STATUS:
            if i[0] == self.status:
                return i[1]

    @staticmethod
    def getOrCreateCartByUser(user):
        try:
            cart = Cart.objects.get(user=user, is_ordered=False)
            return cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
            return cart

    def getCartItems(self):
        return CartItem.objects.filter(cart=self)

    def getShippingTotal(self):
        items = CartItem.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.art.shipping_fee
        return total

    def getSubTotal(self):
        items = CartItem.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.art.price
        return total

    def getTotalPrice(self):
        items = CartItem.objects.filter(cart=self)
        total = 0
        for item in items:
            total += item.getItemPrice()
        return total

    def __str__(self):
        return f"{self.user.email} - {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=False, blank=False)
    art = models.ForeignKey(Art, on_delete=models.CASCADE, null=False, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def addItemToTheCart(art: Art, user):
        cart = Cart.getOrCreateCartByUser(user)
        CartItem.objects.create(cart=cart, art=art)

    @staticmethod
    def checkIfItemIsInCart(art: Art):
        art = CartItem.objects.filter(Q(Q(art=art) & ~Q(cart__status=Cart.CANCELED)))
        return art.exists()

    @staticmethod
    def checkIfUserHaveThatArtInCart(art: Art, user):
        art = CartItem.objects.filter(Q(Q(art=art) & Q(cart__user=user) & ~Q(cart__status=Cart.CANCELED)))
        return art.exists()

    def getItemPrice(self):
        return self.art.price + self.art.shipping_fee

    def __str__(self):
        return f"{self.art.title} - {self.cart.id}"


class wishList(models.Model):
    user = models.ForeignKey(ArtGalleryUsers, on_delete=models.CASCADE, null=False, blank=False)
    art = models.ForeignKey(Art, on_delete=models.CASCADE, null=False, blank=False)
    added_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def getAllWishListItems(user):
        return wishList.objects.filter(user=user)

    @staticmethod
    def checkIfItemIsInWishList(art: Art, user):
        art = wishList.objects.filter(Q(Q(art=art) & Q(user=user)))
        return art

    def __str__(self):
        return f"{self.user.email} - {self.art.title}"


class Blog(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to="blog", null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    blog_category = models.CharField(max_length=100, null=False, blank=False, choices=ART_TYPE, default=PAINTING)
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.CharField(max_length=500, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

    def getDate(self):
        return self.created_at.strftime("%d %b, %Y")

    def getCategoryValue(self):
        for i in ART_TYPE:
            if i[0] == self.blog_category:
                return i[1]

    def getShortDescription(self):
        return self.description[:100]

    def __str__(self):
        return self.title

class Artist(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, unique=True)
    image = models.ImageField(upload_to="blog", null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    blog_category = models.CharField(max_length=100, null=False, blank=False, choices=ART_TYPE, default=PAINTING)
    created_at = models.DateTimeField(auto_now_add=True)
    quote = models.CharField(max_length=500, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    #art = models.ForeignKey(Art, on_delete=models.CASCADE, null=False, blank=False , releated_name="artist")
    
    
    def getDate(self):
        return self.created_at.strftime("%d %b, %Y")

    def getCategoryValue(self):
        for i in ART_TYPE:
            if i[0] == self.blog_category:
                return i[1]

    def getShortDescription(self):
        return self.description[:100]

    def __str__(self):
        return self.title

class contactUs(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    subject = models.CharField(max_length=200, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    phone = models.CharField(max_length=20, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    isContacted = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + self.email + " - " + self.subject

    def validate(self):
        errors = []
        if len(self.name) < 3:
            errors.append("Name must be at least 3 characters long")
        if len(self.subject) < 3:
            errors.append("Subject must be at least 3 characters long")
        
        return errors

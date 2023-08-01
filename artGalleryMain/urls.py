from django.urls import path, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from .Views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
                  path("api/", include("artGalleryApp.urls")),
                  path("", index, name="index2"),
                  path("index", index, name="index"),
                  path("productDetail/<str:title>", productDetail, name="product"),
                  path("addToCart/<str:title>", addToCart, name="addToCart"),
                  path("pageNotFound", pageNotFound, name="pageNotFound"),
                  path("admin", admin.site.urls, name="index"),
                  path("store", store, name="store"),
                  path("removeItem/<int:idItem>", removeItem, name="removeItem"),
                  path("addTowishList/<str:title>", addToWishList, name="removeItem"),
                  path("cart", cart, name="cart"),
                  path("wishlist", wishlist, name="wishlist"),
                  path("checkout", checkout, name="checkout"),
                  path("contactus", contactus, name="contactus"),
                  path("orders", orders, name="orders"),
                  path("Login", Login, name="Login"),
                  path("logout", Logout, name="logout"),
                  path("Signup", Signup, name="Signup"),
                  path("Blog", Blogs, name="blog"),
                  path("Artist", Artists, name="artist"),
                  path("Artist/<str:title>", showArtist, name="artist"),
                  path("invoice/<int:id>", invoice, name="invoice"),
                  path("Blog/<str:title>", showBlogs, name="blog"),
                  path("chatbot", chatbot, name="chatbot"),
                  path("service", service , name="service"),
                  path('resetpassword/',
                       auth_views.PasswordResetView.as_view(template_name="RESET_EMAIL/passwordresetpage.html",
                                                            html_email_template_name="RESET_EMAIL/resetmail.html",
                                                            ),
                       name="reset_password"),
                  path('accounts/password_reset_sent/',
                       auth_views.PasswordResetDoneView.as_view(template_name="RESET_EMAIL/PasswordresetmailSent.html"),
                       name="password_reset_done", ),

                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name="RESET_EMAIL/newpasswordtemplateBack.html"),
                       name="password_reset_confirm"),
                  path('reset_password_complete/',
                       auth_views.PasswordResetCompleteView.as_view(template_name="RESET_EMAIL/passcompl.html"),
                       name="password_reset_complete"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'artGalleryMain.Views.404_view'

from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from .Views import *
from django.conf import settings

urlpatterns = [
                  path('signUp', signUp.as_view(), name="signUp"),
                  path('login', LoginView, name="login"),
                  path('getPoster', getPoster, name="getPoster"),
                  path('placeOrder', placeOrder, name="placeOrder"),
                  path('getBaseData', getBaseData, name="getBaseData"),
                  path('getOrderHistory', getOrderHistory, name="getOrderHistory"),
                  path('store', store.as_view(), name="app_store"),
                  path('addToCart', addToCart, name="app_store"),
                  path('getTrendingItem', getTrendingItem, name="getTrendingItem"),
                  path('favorite', favorite, name="addToFavorite"),
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

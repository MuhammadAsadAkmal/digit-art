from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpRequest, HttpResponse, BadHeaderError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from ..models import *


class PasswordReset(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "RESET_EMAIL/passwordresetpage.html")

    def post(self, request):
        password_reset_form = request.POST["email"]

        if len(password_reset_form) > 0:
            user = ArtGalleryUsers.objects.get(email=password_reset_form)

            if user:
                subject = "Password Reset Requested"
                email_template_name = "RESET_EMAIL/resetmail.html"

                email_details = {
                    "email": password_reset_form,
                    "domain": request.META["HTTP_HOST"],
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }

                email = render_to_string(email_template_name, email_details)

                try:
                    send_mail(subject, email, DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect("accounts/password_reset_sent/")
            else:
                return HttpResponse("You are not authorized to view this page.")
        else:
            redirect("accounts/password_reset_sent/")

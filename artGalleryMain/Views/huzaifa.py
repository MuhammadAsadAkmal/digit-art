from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

from ..Validation.UserValidation import checkUserPermission
from ..models import *
from artGalleryMain.Validation.FormValidation import singUpValidation, loginValidation




def Login(request):
    if request.method == 'POST':
        errors, user = loginValidation(request.POST)
        if len(errors) > 0:
            for err in errors:
                messages.error(request, err)
            print(errors)
            return render(request, 'main/auth/login.html', {
                'data': request.POST
            })
        else:
            password = request.POST['password']
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, 'main/auth/login.html')


def Signup(request):
    if request.method == 'POST':
        print(request.POST)
        validationErrors, user = singUpValidation(request.POST)
        if len(validationErrors) > 0:
            for error in validationErrors:
                messages.error(request, error)
            return render(request, 'main/auth/signup.html', {
                'data': request.POST
            })
        else:
            user.save()
            messages.success(request, "User created successfully")
            return redirect('Signup')
    return render(request, 'main/auth/signup.html')


def Logout(request):
    logout(request)
    return redirect('/')


def Blogs(request):
    blogs = Blog.objects.all().order_by('-id')
    return render(request, 'main/blogList.html', {
        'blogs': blogs
    })


def Artists(request):
    
    artists = Artist.objects.all().order_by('-id')
    return render(request, 'main/artistlist.html', {
        'artists': artists
    })
   


@login_required(login_url='/Login')  # redirect when user is not logged in
@user_passes_test(checkUserPermission, login_url="/Login")
def invoice(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user)
        return render(request, 'main/Invoice.html', {
            'cart': cart
        })

    except Cart.DoesNotExist:
        return redirect('pageNotFound')


def showBlogs(request, title):
    try:
        blog = Blog.objects.get(title=title)
        recentBlogs = Blog.objects.filter(~Q(title=blog.title)).order_by('-id')[:4]
        return render(request, 'main/Blog.html', {
            'blog': blog,
            'recentBlogs': recentBlogs
        })
    except Blog.DoesNotExist:
        return redirect('pageNotFound')


def showArtist(request, title):
    try:
        artist = Artist.objects.get(title=title)
        recentArtists = Blog.objects.filter(~Q(title=artist.title)).order_by('-id')[:4]
        return render(request, 'main/Artist.html', {
            'artist': artist
            
        })
    except Artist.DoesNotExist:
        return redirect('pageNotFound')

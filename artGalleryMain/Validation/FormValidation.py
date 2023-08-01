from ..models import *


def singUpValidation(data):
    username = data['username'].strip()
    full_name = data['full_name'].strip()
    email = data['email'].strip()
    password = data['password'].strip()
    confirmPassword = data['confirmPassword'].strip()
    phone = data['phone'].strip()
    errors = []
    isUsernameExist = ArtGalleryUsers.objects.filter(username=username).exists()
    isEmailExist = ArtGalleryUsers.objects.filter(email=email).exists()
    if isUsernameExist:
        errors.append("Username already exist")
    if isEmailExist:
        errors.append("Email already exist")
    if password != confirmPassword:
        errors.append("Password and confirm password not match")
    elif len(password) < 8:
        errors.append("Password must be 8 characters long")
    if len(phone) != 11:
        errors.append("Phone number must be 11 digits")
    user = ArtGalleryUsers()
    user.username = username
    user.full_name = full_name
    user.email = email
    user.phone = phone
    user.set_password(password)
    return errors, user


def loginValidation(data):
    email = data['email'].strip()
    password = data['password'].strip()
    errors = []
    if len(email) == 0:
        errors.append("Email is required")
    if len(password) == 0:
        errors.append("Password is required")
    user = ArtGalleryUsers.objects.filter(email=email)
    if user.count() == 0:
        errors.append("email or password is incorrect")
    else:
        user = user.first()
        if user.roles != USER:
            errors.append("email or password is incorrect")
    return errors, user


def CheckOutValidation(data):
    address1 = data['address1'].strip()
    address2 = data['address2'].strip()
    postal_code = data['postal_code'].strip()
    city = data['city'].strip()
    country = data['country'].strip()
    errors = []
    if len(address1) == 0:
        errors.append("Address1 is required")
    if len(address2) == 0:
        errors.append("Address2 is required")
    if len(postal_code) == 0:
        errors.append("Postal code is required")
    if len(city) == 0:
        errors.append("City is required")
    if len(country) == 0:
        errors.append("Country is required")
    address = Address()
    address.address1 = address1
    address.address2 = address2
    address.postal_code = postal_code
    address.city = city
    address.country = country

    return errors , address

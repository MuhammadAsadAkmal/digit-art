from ..models import *


def checkUserPermission(user: ArtGalleryUsers):
    return user.roles == USER

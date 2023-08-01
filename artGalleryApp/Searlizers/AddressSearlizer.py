from rest_framework import serializers

from artGalleryMain.models import Art, Address


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"



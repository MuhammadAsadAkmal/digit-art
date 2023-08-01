from rest_framework import serializers

from artGalleryMain.models import Art, wishList, Cart, CartItem


class ArtSerializer(serializers.ModelSerializer):
    pointList = serializers.SerializerMethodField()
    isFavorite = serializers.SerializerMethodField()

    def get_isFavorite(self, obj):
        return wishList.objects.filter(user=self.context.get("user"), art=obj).exists()

    def get_pointList(self, obj):
        return obj.getPointList()

    class Meta:
        model = Art
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Cart


class CartItemSerializer(serializers.Serializer):
    art = ArtSerializer()
    cart = CartSerializer()
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id


    class Meta:
        fields = "__all__"
        model = CartItem

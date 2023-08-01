from rest_framework import serializers

from artGalleryMain.models import HomePagePoster


class HomePagePosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomePagePoster
        fields = "__all__"


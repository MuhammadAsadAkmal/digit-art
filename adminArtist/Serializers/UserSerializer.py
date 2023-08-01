from rest_framework import serializers

from artGalleryMain.models import ArtGalleryUsers


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    dp = serializers.ImageField(required=False)
    phone = serializers.CharField(required=True)

    class Meta:
        model = ArtGalleryUsers
        fields = ['id', 'email', 'password', "username", 'roles', 'full_name', 'dp', "gender", "phone"]
        extra_kwargs = {'password': {'write_only': True, 'required': True},

                        }

    def create(self, validated_data):
        user = ArtGalleryUsers.objects.create_user(**validated_data)
        return user

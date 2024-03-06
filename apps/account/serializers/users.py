from ..models import CustomUser

from rest_framework import serializers


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "full_name",
            "avatar",
            "dob",
            "address",
            "city",
            "state",
            "country",
            "phone_number",
        ]
        extra_kwargs = {
            "email": {"read_only": True},
        }

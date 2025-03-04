from rest_framework import serializers
from auth_api.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id_type = serializers.ChoiceField(choices=User.ID_TYPES)

    class Meta:
        model = User
        fields = ('id_type', 'email', 'phone', 'password')
        extra_kwargs = {
            'email': {'required': False},
            'phone': {'required': False}
        }

    def validate(self, data):
        if data['id_type'] == 'email' and not data.get('email'):
            raise serializers.ValidationError("Email is required for email ID type")
        if data['id_type'] == 'phone' and not data.get('phone'):
            raise serializers.ValidationError("Phone is required for phone ID type")
        return data

class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(write_only=True)
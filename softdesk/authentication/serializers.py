from datetime import date
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from authentication.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'birthdate',
            'can_be_contacted',
            'can_data_be_shared',
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True
            },
            'can_be_contacted': {
                'help_text': 'I agree to be contacted via email'
            },
            'can_data_be_shared': {
                'help_text': (
                    'I agree to my data being shared with'
                    ' a third-party organization'
                )
            }
        }

    def validate_birthdate(selfn, value):
        today = date.today()
        if (
            today.year - value.year - (
                (today.month, today.day) < (value.month, value.day)
            )
        ) < 15:
            raise ValidationError(
                'You must have over 15 years old to create an account'
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

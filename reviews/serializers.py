from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ['user']
        read_only_fields = ['submission_date', 'ip']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Check that start is before finish.
        """
        if data['password'] != data['password']:
            raise serializers.ValidationError("Password and Repeat Password are different")
        return data

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user



class UserRegistrationSerializer(serializers.Serializer):
    '''
    User registration serializer. Used to wrap the Model serializer and provide confirm_password fiedl
    '''
    class Meta:
        write_only_fields = ('password', 'confirm_password')

    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate_email(self, email):
        existing = get_user_model().objects.filter(email=email).first()
        if existing:
            raise serializers.ValidationError("Someone with that email "
                "address has already registered. Was it you?")

        return email

    def validate(self, data):
        if not data.get('password') or not data.get('confirm_password'):
            raise serializers.ValidationError("Please enter a password and "
                "confirm it.")

        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")

        return data

    def save(self, *args, **kwargs):
        model_serializer = UserSerializer(data=self.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save()
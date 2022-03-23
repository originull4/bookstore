from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash


class UserSerializer(serializers.ModelSerializer):

    gender = serializers.CharField(source='customer.gender', required=False)
    avatar = serializers.ImageField(source='customer.avatar', required=False)
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='id', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ('groups', 'user_permissions',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            raise serializers.ValidationError({'password': 'this field is not allowed'})

        if 'customer' in validated_data: customer = validated_data.pop('customer')
        else: customer = {}

        user = super().update(instance, validated_data)

        if 'gender' in customer:
            user.customer.gender = customer['gender']
        if 'avatar' in customer:
            user.customer.avatar = customer['avatar']
        
        user.customer.save()
        return user
       

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=255)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get(
                'request'), username=username, password=password)
            if not user:
                msg = 'unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        return user

class PasswordChangeSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "password fields didn't match."})
        return attrs

    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        update_session_auth_hash(self.context['request'], instance)
        return instance
from rest_framework import serializers

from .models import User
class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
    
    def validate_user(self, value):
        if not User.objects.get(name=value):
            raise serializers.ValidationError('user doesnt exist')
        return value

from rest_framework import serializers

from apps.core.models.user import User, UserSetting


class UserSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSetting
        fields = ('language', 'timezone', 'theme', 'notifications_enabled')


class UserSerializer(serializers.ModelSerializer):
    settings = UserSettingSerializer(required=False)
    orgs = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'phone', 'first_name', 'last_name', 'full_name',
                  'role', 'is_active', 'orgs', 'settings',
                  'phone_is_verified', 'mail_is_verified', 'current_org')
        read_only_fields = ('phone_is_verified', 'mail_is_verified')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_orgs(self, obj):
        return obj.orgs.values('id', 'name')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        if settings_data:
            UserSetting.objects.create(user=user, **settings_data)
        return user

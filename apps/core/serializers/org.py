from rest_framework import serializers

from apps.core.models.org import OrgSetting, Org
from apps.core.serializers.base import BaseModelSerializer


class OrgSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgSetting
        fields = ('language', 'timezone', 'decimal_precision')


class OrgSerializer(BaseModelSerializer):
    settings = OrgSettingSerializer(required=False)
    user_count = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = Org
        fields = BaseModelSerializer.Meta.fields + ('name', 'address', 'note', 'settings', 'user_count')

    def get_user_count(self, obj):
        return obj.user_set.count()

    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        org = super().create(validated_data)
        if settings_data:
            OrgSetting.objects.create(org=org, **settings_data)
        return org

from rest_framework import serializers

from apps.core.models.org import OrgSetting, Org


class OrgSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgSetting
        fields = ('language', 'timezone', 'decimal_precision')


class OrgSerializer(serializers.ModelSerializer):
    settings = OrgSettingSerializer(required=False)

    class Meta:
        model = Org
        fields = ('name', 'address', 'note', 'settings')

    def create(self, validated_data):
        settings_data = validated_data.pop('settings', None)
        org = super().create(validated_data)
        if settings_data:
            OrgSetting.objects.create(org=org, **settings_data)
        return org

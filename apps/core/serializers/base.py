from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """Base serializer for models inheriting from BaseModel"""
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    updated_by_email = serializers.EmailField(source='updated_by.email', read_only=True)
    org_name = serializers.CharField(source='org.name', read_only=True)

    class Meta:
        read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'org')
        fields = ('id', 'created_at', 'updated_at', 'created_by_email',
                  'updated_by_email', 'org_name', 'active')

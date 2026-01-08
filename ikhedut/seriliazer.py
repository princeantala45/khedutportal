from rest_framework import serializers
from ikhedut.models import Contact

class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Contact
        fields="__all__"
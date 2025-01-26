from django.contrib.auth.models import User
from rest_framework import serializers

from .models import TariffPlan, Simcard


class TariffPlanSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = TariffPlan
        fields = '__all__'


class SimcardSerializer(serializers.ModelSerializer):
    TariffPlan = TariffPlanSerializer()

    class Meta(object):
        model = Simcard
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('username', )

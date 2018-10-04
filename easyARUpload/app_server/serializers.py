from rest_framework import serializers
from django.contrib.auth.models import User
from app_server.models import *
from django.core.mail import EmailMessage
from django.conf import settings


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category

class CampaignSerializer(serializers.ModelSerializer):
	class Meta:
		model = Campaign
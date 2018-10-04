# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from app_server.models import *
from django.http import Http404, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.core import serializers
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
import json
from django.forms.models import model_to_dict

from serializers import *

# Create your views here.

class CategoryList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

	# def list(self, request):
	# 	#data = self.get_queryset()
	# 	#data = [(date, Roadshow.objects.filter(from_date__year=date.year, from_date__month=date.month)) for date in Roadshow.objects.dates('from_date', 'month')]
	# 	categories = Category.objects.all()
	# 	return Response(categories)


class CampaignList(APIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )
	queryset = Campaign.objects.all()
	serializer_class = CampaignSerializer

	def post(self, request, format=None):
		request.data['user'] = request.user.id
		print "request_data --->", request.data
		serializer = CampaignSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, format=None):
		campaignlist = Campaign.objects.filter(user=request.user)
		parent_list = []
		print "campaign --->", campaignlist
		for campaign in campaignlist:
			campaign_dict = {}
			campaign_dict['id'] = campaign.id
			campaign_dict['title'] = campaign.title
			campaign_dict['description'] = campaign.description
			campaign_dict['image'] = request.build_absolute_uri(
				'{0}{1}'.format(settings.MEDIA_URL, str(campaign.image)))
			campaign_dict['category'] = campaign.category.name
			campaign_dict['category_id'] = campaign.category.id
			campaign_dict['video'] = request.build_absolute_uri(
				'{0}{1}'.format(settings.MEDIA_URL, str(campaign.video))) if campaign.video else None
			campaign_dict['video_URL'] = campaign.video_URL if campaign.video_URL else None
			campaign_dict['targetID'] = campaign.targetID
			campaign_dict['formData'] = campaign.formData if campaign.formData else None
			campaign_dict['fullScreen'] = campaign.fullScreen
			parent_list.append(campaign_dict)
		return Response(parent_list)


class CampaignView(APIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )

	# def put(self, request, pk ):
	# 	campaign_obj = Campaign.objects.get(id = pk)
	# 	print campaign_obj
	# 	campaign_obj.title = request.data['title']
	# 	campaign_obj.description = request.data['description']
	# 	campaign_obj.category = Category.objects.get(id=request.data['category'])
	# 	campaign_obj.image = request.data['image']
	# 	if request.data['video']:
	# 		campaign_obj.video = request.data['video']
	# 	if request.data['video_URL']:
	# 		campaign_obj.video_URL = request.data['video_URL']

	# 	campaign_obj.save()
	# 	return Response("Campaign updated successfully")


	def put(self, request, pk, format=None):
		# Assign the created by user
		print "request data--->", request.data
		obj = Campaign.objects.get(id=pk)
		serializer = CampaignSerializer(obj, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, pk):
		campaign_obj = Campaign.objects.get(id = pk)
		campaign_obj.delete()
		return Response("Campaign deleted successfully")
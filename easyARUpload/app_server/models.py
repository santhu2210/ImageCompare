# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# from PIL import Image
from django.contrib.auth.models import User, Group

import cv2, os
from easyARServer import *
from PIL import Image

# Create your models here.


class Category(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name_plural = 'category'
        # verbose_name = 'categorys'

class Campaign(models.Model):
	title = models.CharField(max_length=150)
	image = models.ImageField(upload_to='Images/%Y/%m/%d', blank=True)
	description = models.TextField(null=True, blank = True)
	category = models.ForeignKey(Category, related_name='campaignCategory',on_delete=models.CASCADE)
	video = models.FileField(upload_to='video/%Y/%m/%d',blank=True)
	video_URL = models.CharField(max_length=950,null=True,blank = True)
	targetID = models.CharField(max_length=50,null=True,blank = True)
	user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	formData = models.TextField(null=True, blank = True)
	fullScreen = models.BooleanField(default=False)

	# def save(self):
	# 	if not self.id and not self.image:
	# 		return

	# 	super(Campaign, self).save()

	# 	# new_image = Image.open(self.image)
	# 	# (width, height) = new_image.size
	# 	# size = ( width / factor, height / factor)
	# 	# size = (300,300)
	# 	# re_img = new_image.resize(size, Image.ANTIALIAS)
	# 	# re_img.save(self.image.path)

	# 	srcBGR = cv2.imread(self.image.path)
	# 	destRGB = cv2.cvtColor(srcBGR, cv2.COLOR_BGR2RGB)
	# 	cv2.imwrite(self.image.path,destRGB)
	class Meta:
		verbose_name_plural = 'Campaign'

class UserLogin(models.Model):
    user = models.ForeignKey(User) 
    timestamp = models.DateTimeField()


class UserPasswordToken(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=150)

from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, post_delete, pre_delete, pre_save


@receiver(post_save, sender=Campaign)
def addCloudEntry(sender, instance=None, created=False, **kwargs):
	imgDim = Image.open(instance.image)
	print "instance.image -->", instance.image
	width, height = imgDim.size			# checking wheather img in lesser than 2 mb for easyAR
	if (width > 1500 and height > 2000):
		print "inside width , height "
		insImagpath = cv2.imread(instance.image.path)
		resized_image = cv2.resize(insImagpath, (width/2, height/2))
		cv2.imwrite(instance.image.path,resized_image) 

	if created:
		print "inside create"
		similar_response = similar_img(instance) 
		print "similar_response --->", similar_response
		# print "similar status response----> ", similar_response['result']['results'] , len(similar_response['result']['results'])
		# if len(similar_response['result']['results']) == 0:
		cloudresponse = addTarget(instance)
		if (cloudresponse['statusCode'] != -1):
			targetid =  cloudresponse['result']['targetId']
			instance.targetID = targetid
			instance.save()
		else:
			instance.delete()


@receiver(post_delete, sender=Campaign)
def deletecloudEntry(sender, instance, **kwargs):
	print instance.title , instance.targetID
	cloudresponse = deleteTarget(instance) if instance.targetID else None
	# instance.delete()
	print cloudresponse
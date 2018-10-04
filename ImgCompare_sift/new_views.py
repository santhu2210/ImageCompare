# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from appserver.models import *
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
from PIL import Image
import cv2, os
import numpy as np
#from matplotlib import pyplot as plt

# Create your views here.


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


class CheckingList(APIView):
	permission_classes = (IsAuthenticated, )
	authentication_classes = (JSONWebTokenAuthentication, )

	def post(self, request, format=None):
		request.data['user'] = request.user.id
		req_img  = request.data['file']

		im = Image.open(req_img)
		width, height = im.size
		#print "request_data --->", req_img , width, height

		images_path = './Images/'
		files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path)) ]

		target_img = req_img

		#rol = match(files, target_img)
		data = feature_match(files, target_img)

		if data['name']:
			imgPath = data['name'][2:]
			campaign = Campaign.objects.get(image=imgPath)
			if campaign:				
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
				campaign_dict['centerPoint'] = data['centerPoint']

				return Response(campaign_dict)


		return Response({"Results":data})





def match(files, target ):

	print "files" , type(files), type(target)

	for s in files:
		print "Query images  on ==" , s

		img_rgb = cv2.imread(s)
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		img2 = img_rgb.copy()

		#print "source image size gray -->", img_gray.shape
		tar_im = Image.open(target).convert('L')   # read target image as gray scale
		template = np.array(tar_im)
		#print "target image size -->", template.shape 

		#template =  cv2.imdecode(np.fromstring(target.read(), np.uint8), cv2.IMREAD_UNCHANGED)
		#template = cv2.imread(target, 0) # 0, it read grayscale by default

		w,h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray,template, cv2.TM_CCOEFF_NORMED) # TM_SQDIFF TM_CCOEFF_NORMED TM_CCORR_NORMED
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		thresold = 0.80
		loc = np.where(res >= thresold)
		if loc[0].size > 10:
			top_left = max_loc
			bottom_right = (top_left[0]+w, top_left[1]+h)
			cv2.rectangle(img2, top_left, bottom_right, (0,255,255), 2)

			cv2.imwrite('train_detect_img.jpg', img2)

			# plt.imshow(img2)
			# plt.show()
			return (top_left, bottom_right)

	print "nothing matched"
	return((0,0),(0,0))



# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()
    

def feature_match(files, target):    

    #img1 = cv2.imread(target,0)   # qurey image
    tar_im = Image.open(target).convert('L')   # read target image as gray scale
    img1 = np.array(tar_im)

    for s in files:
        print "matching image on %s" % s
        img2 = cv2.imread(s,0)
        #orb = cv2.ORB_create()
        #
        #kp1, des1 = orb.detectAndCompute(img1, None)
        #kp2, des2 = orb.detectAndCompute(img2, None)
        #
        #bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        #
        #matches = bf.match(des1, des2)
        #
        #matches = sorted(matches, key = lambda x:x.distance)
        
        #img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:6],None, flags = 2)
        #
        #cv2.imwrite('feature_detect_img.jpg', img3)
        # 
        #plt.imshow(img3),plt.show()       
     
       
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(img1,None)
        kp2, des2 = sift.detectAndCompute(img2,None)
        
        ### BFMatcher with default params
        ##bf = cv2.BFMatcher()
        ##matches = bf.knnMatch(des1,des2, k=2)
        
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks=50)   # or pass empty dictionary
        
        flann = cv2.FlannBasedMatcher(index_params,search_params)
        
        matches = flann.knnMatch(des1,des2,k=2)
        
        
        # Apply ratio test
        good = []
        knnlst = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append(m)
                knnlst.append([m])
        
        
        if len(good) > 20:
            # cv2.drawMatchesKnn expects list of lists as matches.
            
            #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,knnlst,None,flags=2)   # match distances
            
            rows2 = img2.shape[0]
            cols2 = img2.shape[1]
            
            out = np.zeros((max([rows2]),cols2,3), dtype='uint8')
            
            # Place the first image to the left
            #out[:rows1, :cols1] = np.dstack([img1])
            
            # Place the next image to the right of it
            out[:rows2, :cols2] = np.dstack([img2])
            
            chker = []    
            
            for mat in good:
                # Get the matching keypoints for each of the images
                #img1_idx = mat.queryIdx
                img2_idx = mat.trainIdx
                
                # x - columns
                # y - rows
                #(x1,y1) = kp1[img1_idx].pt
                (x2,y2) = kp2[img2_idx].pt
                
                # Draw a small circle at both co-ordinates
                # radius 4
                # colour green
                # thickness = 1
                chker.append((x2,y2))
                cv2.circle(out, (int(x2),int(y2)), 3, (0, 255, 0), 1)
            
            #plt.imshow(out,),plt.show()
            #cv2.imwrite('feature_out_img.jpg', out)
            
            #cv2.imwrite('feature_detect_img.jpg', img3)
            
            #plt.imshow(img3),plt.show()
            
            if chker:
                min_x = int(min(chker, key=lambda x: x[0])[0])
                max_x = int(max(chker, key=lambda x: x[0])[0])
                min_y = int(min(chker, key=lambda x: x[1])[1])
                max_y = int(max(chker, key=lambda x: x[1])[1])
                
                top_left = (min_x, min_y)
                bottom_right = (max_x, max_y)
                center_point = ((min_x+max_x)/2, (min_y+max_y)/2)
                
                cv2.rectangle(out,top_left, bottom_right, (0,255,255), 2)
                cv2.circle(out, center_point, 5, (255, 0, 0), 1)
                
                cv2.imwrite('feature_box_img.jpg', out)
                
                #plt.imshow(out,),plt.show()
                data = {"name": s, "centerPoint": center_point, "topLeft": top_left, "bottomRight": bottom_right}
                return data
    print "nothing mached"

    data = {"Image": None, 'center_point':(0,0)}

    return(data)
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

# Register your models here.

from models import *
from django.utils.html import format_html
from django.contrib.auth import get_user_model

class ImgModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = super(ImgModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def image_tag(self, obj):
        return format_html('<img src="{}" width="120" height="120" /> <p>{}</p>'.format(obj.image.url, obj.title))

    image_tag.short_description = 'Image'
    list_display = ['image_tag',]
    exclude = ['user',]
    readonly_fields=('targetID', )

    def get_fields(self, request, obj=None):
        if obj is None:
            return ('title','image','description','category','video','video_URL','formData','fullScreen')
        return ('title','image','description','category','video','video_URL','targetID','fullScreen')

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super(ImgModelAdmin, self).save_model(request, obj, form, change)

admin.site.register(Campaign, ImgModelAdmin)   # rewrite the Campaign model using admin model
	
admin.site.register(Category)



    # def get_changeform_initial_data(self, request):
    #     get_data = super(ImgModelAdmin, self).get_changeform_initial_data(request)
    #     get_data['user'] = request.user.pk
    #     print "inside getchange", request.user.pk , get_data
    #     return get_data

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'user':
    #         kwargs['queryset'] = get_user_model().objects.filter(username=request.user.username)
    #     return super(ImgModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    # def get_readonly_fields(self, request, obj=None):
    #     if obj is not None:
    #         return self.readonly_fields + ('user',)
    #     return self.readonly_fields

    # def add_view(self, request, form_url="", extra_context=None):
    #     data = request.GET.copy()
    #     data['user'] = request.user
    #     request.GET = data
    #     return super(ImgModelAdmin, self).add_view(request, form_url="", extra_context=extra_context)


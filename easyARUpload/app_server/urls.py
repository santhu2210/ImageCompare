from django.conf.urls import url
from . import views
from rest_framework_jwt.views import obtain_jwt_token
import app_server

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^category/$', views.CategoryList.as_view()),
    url(r'^campaign/$', views.CampaignList.as_view()),
    url(r'^campaign/(?P<pk>[0-9]+)/$', views.CampaignView.as_view()),

]
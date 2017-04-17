from django.conf.urls import url

from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chat/receive/(\w*)$',views.process_message, name='recieve'),
]
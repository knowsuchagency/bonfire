from django.conf.urls import url
from tinder import views


urlpatterns = [
    url('^', views.index, name="index")
]
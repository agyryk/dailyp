from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.homeView, name='homeView'),
    url(r'^category/$', views.categoryView, name='categoryView'),
    url(r'^test/$', views.testView, name='testView')
]
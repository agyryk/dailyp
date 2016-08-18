from django.conf.urls import url
from . import views
from . import  api_views


urlpatterns = [
    url(r'^$', views.homeView, name='homeView'),
    url(r'^category/$', views.categoryView, name='categoryView'),
    url(r'^test/$', views.testView, name='testView'),
    url(r'^postrun/$', api_views.Poster.as_view(), name='postView')
]
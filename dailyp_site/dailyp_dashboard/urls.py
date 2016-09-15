from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.homeView, name='homeView'),
    url(r'^details/$', views.composedView, name='composedView'),
    url(r'^history/$', views.historyView, name='historyView'),
]

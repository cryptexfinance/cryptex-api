from django.urls import path
from django.urls import re_path
from . import views


app_name = 'governance'

urlpatterns = [
    re_path(
        r'^create/$',
        views.CreateKeeper.as_view(),
        name='create'
    ),
    re_path(
        r'^update/$',
        views.UpdateKeeper.as_view(),
        name='update'
    ),
    re_path(
        r'^all/$',
        views.KeepersAll.as_view(),
        name='all'
    ),
]
from __future__ import absolute_import

from django.urls import path

from .. import views

app_name = 'accessmap'

urlpatterns = [
    path('map/', views.MapIndexVies, name='map'),
    path('map/map_render.html', views.MapRenderIndexVies, name='map_render'),
    path('map/map_view', views.MapView, name='map_view'),
    path('stat/', views.StatIndexVies, name='stat'),
    path('stat/daystat.html', views.DayStatIndexVies, name='daystat'),
]

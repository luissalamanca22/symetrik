

from importer.api import views
from django.conf.urls import url
from rest_framework import routers

urlpatterns = [
    url(r'^query_table/(?P<tablename>\w+)/$', views.ImportedTablesApiView.as_view(), name="query_table"),
]

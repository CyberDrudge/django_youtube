from django.urls import path
from .views import (
	VideoListView,
	VideoSearchView
)

app_name = 'products'

urlpatterns = [
	path('', VideoListView.as_view(), name='list'),
	path('search', VideoSearchView.as_view(), name='search'),
]

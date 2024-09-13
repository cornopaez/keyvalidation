from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	path('accounts/', views.AccountList.as_view()),
	path('key_creation/', views.AccountAndKeyApiView.as_view()),
	path('key_list', views.KeyGroupApiView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

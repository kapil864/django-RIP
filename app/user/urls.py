"""
URL mapping for the user API
"""

from django.urls import path

from user import views

app_name = 'user'


urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', view=views.CreateTokenView.as_view(), name='token'),
    path('me/', view=views.ManageUserView.as_view(), name='me'),
]

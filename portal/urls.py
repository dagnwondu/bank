from  django.urls import path
from . import views
app_name = 'portal'
urlpatterns = [
    # Define your URL patterns here
    path('', views.customer_dashboard, name='customer_dashboard'),
]
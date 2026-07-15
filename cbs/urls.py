from  django.urls import path
from . import views
app_name = 'cbs'

urlpatterns = [
    path('api/accounts/<str:account_number>/', views.mock_t24_api_account_balance, name='mock_t24_api'),
]
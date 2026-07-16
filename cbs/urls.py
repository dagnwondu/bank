from  django.urls import path
from . import views
app_name = 'cbs'


urlpatterns = [
    # Changed from account_number to customer_id for clarity
    path('api/accounts/<str:customer_id>/', views.mock_t24_api_account_balance, name='mock_t24_api'),
]
from  django.urls import path
from . import views
app_name = 'portal'

urlpatterns = [
    # Define your URL patterns here
    path('', views.customer_dashboard, name='customer_dashboard'),
    path('fund_transfer_page/', views.fund_transfer_page, name='fund_transfer_page'),
    path('transactions/partial/', views.transaction_list_partial, name='transaction_list_partial'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('customers/', views.CustomerListCreateAPIView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', views.CustomerRetrieveUpdateDeleteAPIView.as_view(), name='customer-detail'),
    path('orders/', views.OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', views.OrderRetrieveUpdateDeleteAPIView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.OrderStatusUpdateAPIView.as_view(), name='order-status-update'),
]
 
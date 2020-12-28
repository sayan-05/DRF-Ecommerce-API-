from django.urls import path
from django.urls.conf import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('data', GetProduct, name='product-api'),
    path('create', CreateProduct, name='create-product'),
    path('edit/<str:pk>/', EditProduct, name='edit-product'),
    path('delete/<str:pk>/', DeleteProduct, name='delete-product'),
    path('', ProductApiRoutes, name='api-routes'),
    path('register', CreateUserView.as_view()),
    path('token-auth', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-order-item/<str:id>/', get_order_item),
    path('get-checkout-order-item/<str:id>/', get_checkout_order_item),
    path('set-order-item', set_order_item),
    path('get-user-id/<str:username>/', get_user_id),
    path('update-order', update_order),
    path('get-total-value/<str:id>/', get_total_value),
    path('set-ordered-products/<str:id>/', set_ordered_products),
    path('delete-order', delete_ordered_products),
    path('set-bought-item', set_bought_item),
    path('get-bought-item', get_bought_item),
]

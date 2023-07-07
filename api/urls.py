from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='refresh'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # USER
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),


    # Categories
    path('categories/', views.categories_list_view, name='categories-list'),
    # Categories



    # products/?ids= || products/?q="name/s   ?q=منتج&category=اج"   ?min_sell_price=2&max_sell_price=22
    path('products/', views.ProductView.as_view(), name='product-list'),

    #RATING
    #if need to comment {"comment":"test"}
    path('products/<int:product_id>/ratings/<int:user_id>/<int:rating>/', views.ProductRatingView.as_view()),


    # State
    path('states/', views.StateList.as_view(), name='state-list'),

    # see the cart item for the user
    path('cart/user/<int:user_id>/', views.CartView.as_view(), name='cart'),
    # update or create cart item {quantity:2} for ex
    path('cart/user/<int:user_id>/product/<int:product_id>/var/<int:Var_id>/',
         views.CartItemView.as_view(), name='cart_item'),
    # delete cart item
    path('cart/user/<int:user_id>/cartitem/<int:item_id>/delete/',
         views.CartItemDeleteView.as_view(), name='cartitem-delete'),
    # delete all cart items
    path('carts/<int:user_id>/', views.CartListView.as_view(), name='cart-list'),


    #     {
    #       "user": 1,
    #        "name":"test",
    #        "shipping_address": "add3",
    #        "shipping_address2": "add2",
    #        "phone": "22",
    #        "phone2": "33",
    #        "shipping_to":1,
    #       "order_items": [
    #         {
    #           "product": 20,
    #           "Var": 2,
    #           "quantity": 1,
    #         }
    #       ]
    #     }
    # ORDER CREATE POST
    path(
        'orders/', views.OrderViewSet.as_view({'get': 'list'}), name='order-list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create-order'),
    # ?date=2022-06-01&status=arrived
    path('users/<int:user_id>/orders/', views.UserOrderList.as_view(), name='user_order_list'),
]

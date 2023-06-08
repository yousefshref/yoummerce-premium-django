from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.contrib.auth import login, get_user_model
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Cart, CartItem, Order, State,OrderItem
from .serializers import ProductSerializer, CartSerializer,StateSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer, UserSerializerAll
from django.http import Http404
from rest_framework import generics
from rest_framework import views
from django.utils import timezone
from rest_framework import viewsets, status
from django.db import transaction


# USER
class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializerAll
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        data['is_superuser'] = instance.is_superuser
        data['is_staff'] = instance.is_staff

        return Response(data)
# USER



# STATE
class StateList(APIView):
    def get(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
# STATE

# ORDER
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        order_items_data = request.data.get('order_items')
        if not order_items_data:
            return Response({'error': 'order_items are required'}, status=status.HTTP_400_BAD_REQUEST)

        # If order_items are provided, proceed with creating the order and order_items
        order_serializer = self.get_serializer(data=request.data)
        order_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            order = order_serializer.save()

            for item_data in order_items_data:
                item_data['order'] = order.id
                order_item_serializer = OrderItemSerializer(data=item_data)
                order_item_serializer.is_valid(raise_exception=True)
                order_item_serializer.save()

        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

class UserOrderList(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Order.objects.filter(user_id=user_id)

        # Get the search parameters from the query string
        date = self.request.query_params.get('date', None)
        order_status = self.request.query_params.get('status', None)

        # Filter the queryset based on the search parameters
        if date:
            # Convert the date string to a timezone-aware datetime object
            date_obj = timezone.datetime.strptime(date, '%Y-%m-%d').date()
            queryset = queryset.filter(date_created__date=date_obj)

        if order_status:
            queryset = queryset.filter(order_status=order_status)

        queryset = queryset.order_by('-id')

        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
# ORDER

# CART
class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    
    def get_object(self):
        user_id = self.kwargs['user_id'] 
        return Cart.objects.get(user_id=user_id)

class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_object(self):
        user_id = self.kwargs['user_id']
        item_id = self.kwargs['item_id']
        cart = Cart.objects.get(user_id=user_id)
        item = CartItem.objects.get(id=item_id, cart=cart)
        return item

    def delete(self, request, *args, **kwargs):
        item = self.get_object()
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Cart.objects.filter(user_id=user_id)

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        carts = Cart.objects.filter(user_id=user_id)
        for cart in carts:
            cart.cart_items.all().delete()
        return Response({"message": "Cart items deleted successfully."})


class CartItemView(views.APIView):
    
    def post(self, request, user_id, product_id, Var_id):
        # Get the user's cart
        cart = Cart.objects.get(user_id=user_id)
        
        # Create or update cart item 
        serializer = CartItemSerializer(data={'product': product_id, 'Var': Var_id, 'quantity': request.data.get('quantity')})
        if serializer.is_valid():
            data = serializer.validated_data
            quantity = data.get('quantity')
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, 
                product_id=product_id,
                Var_id=Var_id
            )        
            cart_item.quantity = quantity   
            cart_item.save()
            return Response(CartSerializer(cart).data)
        else:
            return Response(serializer.errors)
# CART

# PRODUCT
class ProductView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, pk=None):
        # Check if a search query is provided in the 'q' parameter
        search_query = request.GET.get('q', '')

        if pk is not None:
            # If a single ID is provided, retrieve that product
            try:
                product = Product.objects.get(pk=pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                raise Http404
        elif search_query:
            # If a search query is provided, filter the products by name
            products = Product.objects.filter(name__icontains=search_query)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        else:
            # If no ID or search query is provided, retrieve all products
            ids = request.GET.get('ids', '')
            if not ids:
                products = Product.objects.all()
            else:
                # If a comma-separated list of IDs is provided, retrieve those products
                id_list = ids.split(',')
                products = Product.objects.filter(pk__in=id_list)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
# PRODUCT

# Login
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework import serializers
from .models import State, Product, Var, ProductImage, Cart, CartItem, Order, OrderItem, Categories, ProductRating
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model



class UserSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'first_name', 'last_name']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'shipping_price']


# Product
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class VarSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(read_only=True, source='product.id')
    class Meta:
        model = Var
        fields = ['id',"product", 'Var_name', 'buy_price', 'sell_price', 'earning',
                  'consumer_commission', 'stock', 'add_stock', 'remove_stock', 'befor_discount']


class RelatedProductSerializer(serializers.ModelSerializer):
    Var = VarSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'images', 'Var']

class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.CharField()

    class Meta:
        model = ProductRating
        fields = ['id', 'user', 'rating', 'comment', 'reply', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    Var = VarSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.CharField()
    related_products = RelatedProductSerializer(many=True, read_only=True)
    ratings = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()


    def get_average_rating(self, obj):
        ratings = obj.productrating_set.all()
        if ratings:
            rating_sum = sum([rating.rating for rating in ratings])
            return rating_sum / len(ratings)
        else:
            return 0

    def get_ratings(self, obj):
        ratings = obj.productrating_set.all()
        serializer = ProductRatingSerializer(ratings, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category',
                  'related_products', 'Var', 'images', 'ratings','average_rating']

# Product



# Categories
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
# Categories





# CART
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    Var = serializers.SerializerMethodField()
    # total = serializers.IntegerField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id','product', 'Var', 'quantity','total','total_commission']

    def get_product(self, obj):
        return ProductSerializer(obj.product).data

    def get_Var(self, obj):
        return VarSerializer(obj.Var).data


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'cart_items']
# CART


# ORDER
class OrderItemSerializer(serializers.ModelSerializer):
    product_all = ProductSerializer(read_only=True)
    Var_all = VarSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    shipping_to_text = serializers.CharField(source='shipping_to.name', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    user_text = serializers.CharField(
        source='user.username', read_only=True)
    shipping_price = serializers.IntegerField(read_only=True)
    total_order_price = serializers.IntegerField(read_only=True)
    order_status = serializers.CharField(read_only=True)
    total_order_price = serializers.IntegerField()
    date_created = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
# ORDER

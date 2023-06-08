from django.contrib import admin
from .models import Product, ProductImage, Cart, State, Order, CartItem, OrderItem, Var,Categories
from django.db.models import Sum


# PRODUCTS
class ProductImageInline(admin.TabularInline):
    model = ProductImage

class VarInline(admin.TabularInline):
    model = Var

class ProductAdmin(admin.ModelAdmin):
    inlines = [VarInline,ProductImageInline]
    list_display = ['id', 'name', 'category','date_created']
    list_editable = ['name','category']
    search_fields = ['name']
    list_filter = ["date_created"]


class VarAdmin(admin.ModelAdmin):
    list_display = ["product","Var_name", "buy_price","sell_price","earning","consumer_commission","stock","add_stock","remove_stock"]
    list_editable = ["sell_price","consumer_commission","stock","add_stock","remove_stock"]
    search_fields = ['Var_name']

    change_list_template = "admin/var/var_admin.html"

    def changelist_view(self, request, extra_context=None):
        # create an empty dictionary if extra_context is None
        extra_context = extra_context or {}
        # get the filtered queryset
        queryset = self.get_queryset(request)
        # aggregate the sums of the relevant fields
        total_buy_price_sum = queryset.aggregate(Sum("buy_price"))["buy_price__sum"]
        total_sellprice_sum = queryset.aggregate(Sum("sell_price"))["sell_price__sum"]
        total_earning_sum = queryset.aggregate(Sum("earning"))["earning__sum"]
        total_consumer_commission_sum = queryset.aggregate(Sum("consumer_commission"))["consumer_commission__sum"]

        # add the sums to the extra context
        extra_context["total_buy_price_sum"] = total_buy_price_sum
        extra_context["total_sellprice_sum"] = total_sellprice_sum
        extra_context["total_earning_sum"] = total_earning_sum
        extra_context["total_consumer_commission_sum"] = total_consumer_commission_sum
        
        # call the parent method with the updated extra context
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Product, ProductAdmin)
admin.site.register(Var,VarAdmin)
admin.site.register(Categories)
# PRODUCTS


# STATES
class StateAdmin(admin.ModelAdmin):
    list_display = ["name","shipping_price"]
    list_editable = ["shipping_price"]


admin.site.register(State,StateAdmin)
# STATES#


# Cart
class CartItemInline(admin.StackedInline):
    model = CartItem
    
class CartAdmin(admin.ModelAdmin):  
    inlines = [CartItemInline]

admin.site.register(Cart, CartAdmin)
# Cart


# ORDER
class OrderItemInline(admin.StackedInline):
    model = OrderItem

    class Meta:
        model = OrderItem
        fields = ['product', 'color', 'quantity']

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'total_earning']
        return fields

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_filter = ["date_created"]
    list_display = ['id','name',"shipping_address","phone" ,"order_status","date_created",'total_order_price' ,"shipping_to"]
    list_editable = ['order_status','shipping_to']
    search_fields = ["name", "phone"]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if 'total_earning' in fields and not request.user.is_superuser:
            fields.remove('total_earning')
        return fields


    change_list_template = "admin/order/order_admin.html"

    def changelist_view(self, request, extra_context=None):
        # create an empty dictionary if extra_context is None
        extra_context = extra_context or {}
        # get the filtered queryset
        queryset = self.get_queryset(request)
        # aggregate the sums of the relevant fields
        total_order_price_sum = queryset.aggregate(Sum("total_order_price"))["total_order_price__sum"]
        
        # print the sums for debugging purposes
        print("total_order_price_sum=", total_order_price_sum)

        # add the sums to the extra context
        extra_context["total_order_price_sum"] = total_order_price_sum
        
        # call the parent method with the updated extra context
        return super().changelist_view(request, extra_context=extra_context)
    
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["id", 'order', "product", "Var", 'quantity', "total_commession"]
    list_editable = ['quantity']
    list_filter = [("order__date_created", admin.DateFieldListFilter)]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'total_earning']
        return fields

    def get_list_display(self, request):
        if request.user.is_superuser:
            # If the user is staff, include the total_earning field in the list_display
            return ["id", 'order', "product", "Var", 'quantity', "total_commession", "total_earning"]
        else:
            # If the user is not staff, exclude the total_earning field from the list_display
            return ["id", 'order', "product", "Var", 'quantity', "total_commession"]


    
    change_list_template = "admin/order_item/order_item_admin.html" # create a custom template

    def get_queryset(self, request):
        # get the default queryset
        qs = super().get_queryset(request)
        # filter out the orders that have no date created
        qs = qs.filter(order__date_created__isnull=False)

        # get the filter parameters from the request
        date_created__gte = request.GET.get("order__date_created__gte")
        date_created__lte = request.GET.get("order__date_created__lte")

        # apply the filters to the queryset
        if date_created__gte:
            qs = qs.filter(order__date_created__gte=date_created__gte)
        if date_created__lte:
            qs = qs.filter(order__date_created__lte=date_created__lte)
        
        return qs

    def changelist_view(self, request, extra_context=None):
        # create an empty dictionary if extra_context is None
        extra_context = extra_context or {}
        # get the filtered queryset
        queryset = self.get_queryset(request)
        # aggregate the sums of the relevant fields
        # total_order_price_sum = queryset.aggregate(Sum("total_order_price"))["total_order_price__sum"]
        total_earning_sum = queryset.aggregate(Sum("total_earning"))["total_earning__sum"]
        total_commession_sum = queryset.aggregate(Sum("total_commession"))["total_commession__sum"]

        # add the sums to the extra context
        # extra_context["total_order_price_sum"] = total_order_price_sum
        if request.user.is_superuser:
            extra_context["total_earning_sum"] = total_earning_sum
        extra_context["total_commession_sum"] = total_commession_sum
        
        # call the parent method with the updated extra context
        return super().changelist_view(request, extra_context=extra_context)

    # DATE
    def get_order_date_created(self, obj):
        return obj.order.date_created
    
    get_order_date_created.admin_order_field = "order__date_created"
    get_order_date_created.short_description = "Order Date Created"
    
admin.site.register(OrderItem, OrderItemAdmin)

# ORDER
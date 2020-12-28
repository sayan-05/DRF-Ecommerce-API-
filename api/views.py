from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from .models import ProductInfo, OrderItem
from rest_framework.views import APIView
# Create your views here.


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def GetProduct(request):
    list = ProductInfo.objects.all()
    serializer = ProductInfoSerializer(list, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def CreateProduct(request):
    serializer = ProductInfoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['POST'])
def EditProduct(request, pk):
    product = ProductInfo.objects.get(id=pk)
    serializer = ProductInfoSerializer(instance=product, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def DeleteProduct(request, pk):
    product = ProductInfo.objects.get(title=pk)
    product.delete()

    return Response('deleted')


@api_view(['GET'])
def ProductApiRoutes(request):
    routes = {
        'All Product': 'api/data',
        'Create Product': 'api/create',
        'Edit Product': 'api/edit/<str:pk>',
        'DeleteProduct': 'api/delete/<str:pk>',
        'Register User': 'api/register',
        'User Login': 'api/token-auth',
        'Current User ID': 'api/get-user-id/<str:username>/',
        'Get User Order Items ': 'api/get-order-item/<str:id>/',
        'Get User Checkout Items ': 'api/get-checkout-order-item/<str:id>/',
        'Set User Order Item': 'api/set-order-item' ,
        'Update Order Item' : 'api/update-order',
        'Get Total Order Value' : 'api/get-total-value/<str:id>/',
        'Delete Order Item' : 'api/delete-order',
        'Set Bought Items' : 'api/set-bought-item',
        'Get Bought Item' : 'api/get-bought-item'        
    }

    return Response(data=routes)


class CreateUserView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        user = request.data.get('user')
        if not user:
            return Response({'response': 'error', 'message': 'No data found'})
        serializer = UserSerializerWithToken(data=user)
        if serializer.is_valid():
            saved_user = serializer.save()
        else:
            return Response({"response": "error", "message": serializer.errors})
        return Response({"response": "success", "message": "user created succesfully"})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_id(request, username):
    query = User.objects.get(username=username)
    serializer = GetUserIdSerializer(query, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_order_item(request, id):
    query = OrderItem.objects.filter(user=id)
    serializer = OrderItemSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_checkout_order_item(request, id):
    query = OrderItem.objects.filter(user=id, proceed=True)
    serializer = OrderItemSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_order_item(request):
    serializer = GetOrderItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.validated_data['item']
        quantity = serializer.validated_data['quantity']
        user = serializer.validated_data['user']
        queryset = OrderItem.objects.filter(user_id=user, item=item)
        if queryset.exists():
            info = queryset[0]
            info.quantity += quantity
            info.save(update_fields=['quantity'])
            return Response("Succesfully created", status=status.HTTP_201_CREATED)
        else:
            serializer.save()
            return Response("Succesfully created", status=status.HTTP_201_CREATED)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_order(request):
    serializer = OrderItemUpdateSerializer(data=request.data)
    if serializer.is_valid():
        item_id = serializer.data['item_id']
        quantity = serializer.data['quantity']
        user_id = serializer.data['user_id']
        proceed = serializer.data['proceed']
        queryset = OrderItem.objects.filter(item_id=item_id, user_id=user_id)
        if queryset.exists():
            item = queryset[0]
            item.quantity = quantity
            item.proceed = proceed
            item.save(update_fields=['quantity', 'proceed'])
            return Response("edited", status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_total_value(request, id):
    price_list = OrderItem.objects.filter(
        user_id=id, proceed=True).values_list('item__price', flat=True)

    filtered_price_list = [s.replace('$', '') for s in price_list]
    int_filtered_price_list = [int(i) for i in filtered_price_list]
    item_quantity = OrderItem.objects.filter(
        user_id=id, proceed=True).values_list('quantity', flat=True)

    total_value_each = [int_filtered_price_list[i] * item_quantity[i]
                        for i in range(len(int_filtered_price_list))]

    total_price = sum(total_value_each)
    cart_length = len(int_filtered_price_list)

    return Response({'total_price': total_price, 'cart_length': cart_length})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def set_ordered_products(request, id):
    query = OrderItem.objects.filter(user=id)
    serializer = OrderItemSerializer(query, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_ordered_products(request):
    serializer = OrderItemDeleteSerializer(data=request.data)
    if serializer.is_valid():
        id = serializer.validated_data['id']
        user_id = serializer.validated_data['user_id']
        query = OrderItem.objects.filter(user=user_id, id=id)
        if query.exists():
            query[0].delete()
            return Response('deleted', status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_bought_item(request):
    serializer = BoughtItemCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        quantity = OrderItem.objects.filter(
            user_id=user, proceed=True).values_list('quantity', flat=True)

        item_list = OrderItem.objects.filter(
            user_id=user, proceed=True).values_list('item__id', flat=True)

        bulk_item_list = [BoughtItem(
            item_id=val, user=user, quantity=quantity) for val in item_list]

        BoughtItem.objects.bulk_create(bulk_item_list)
        OrderItem.objects.filter(
            user_id=user, proceed=True).delete()
        return Response('done')
    else:
        return Response('bad request')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def get_bought_item(request):
    serializer = BoughtItemCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        query = BoughtItem.objects.filter(user_id=user)
        bought_item_get_serializer = BoughtItemGetSerializer(query, many=True)
        return Response(bought_item_get_serializer.data)
    return Response('bad_request')


@api_view(['GET'])
def homepage(request):
    return Response(
        {
            'api': '/api',
            'admin': '/admin'
        }
    )

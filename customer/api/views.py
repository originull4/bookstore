from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from book.api.serializers import BookSerializer
from book.models import Book
from .permissions import IsAdmin, IsAdminOrOwner, IsOwner

from customer.models import OrderItem, Order
from .serializers import OrderItemSerializer, OrderSerializer, UserSerializer, LoginSerializer, PasswordChangeSerializer


class UserCreateAPIView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user).key
            data = {'user': serializer.data, 'token': token}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserListAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        users = User.objects.all()        
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

class UserDetailAPIView(APIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminOrOwner]

    def get(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAdminOrOwner]

    def put(self, request, **kwargs):
        user = get_object_or_404(User, id=kwargs['id'])
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token = Token.objects.get(user=user).key
        data = {
            'id': user.id,
            'username': user.username,
            'token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)


class PasswordChangeAPIView(APIView):
    
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsOwner,]

    def put(self, request, **kwargs):

        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)

        serializer = PasswordChangeSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            msg = {"detail": "password changed successfully"}
            return Response(msg, status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class CartAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        # get user cart
        cart = user.customer.cart
        # get list of books in user's cart
        cart_books = [item.book for item in cart.items.all()]
        serializer = BookSerializer(cart_books, many=True, context={'request': request})
        data = {
            'order_id': cart.order_id,
            'books': serializer.data
        }
        return Response(data=data)


class FakePaymentAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        # get user cart
        order = user.customer.cart
        if order.items.all().count() == 0:
            return Response({'detail': 'ther is not any pending order.'})

        order.amount = user.customer.cart_total_price
        order.complete = True
        order.dete_completed = datetime.now()
        order.save()
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)


class CartAddAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request, *args, **kwargs):
        # add a book to the user's cart.
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        book = get_object_or_404(Book, slug=kwargs['book_slug'])
        cart = request.user.customer.cart
        order_item, created = OrderItem.objects.get_or_create(order=cart, book=book)
        request.user.customer.update_cart_total_price()
        sr = OrderItemSerializer(order_item, context={'request': request})
        return Response(sr.data)


class CartRemoveAPIView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, *args, **kwargs):
        # delete a book from user's cart
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        book = get_object_or_404(Book, slug=kwargs['book_slug'])
        cart = request.user.customer.cart
        order_item = get_object_or_404(OrderItem, order=cart, book=book)
        order_item.delete()
        request.user.customer.update_cart_total_price()
        return Response({f'{book}': 'was deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class OrderedBooksAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        books = user.customer.ordered_books
        if not books:
            return Response({'detail': 'there is not any ordered book.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class OrdersAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        orders = Order.objects.filter(customer=user.customer)
        if not orders:
            return Response({'detail': 'there is not any order.'}, status=status.HTTP_204_NO_CONTENT)
        serializer = OrderSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)


class OrderItemsAPIView(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrOwner]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['id'])
        self.check_object_permissions(request, user)
        try:
            order = get_object_or_404(Order, order_id=kwargs['order_id'])
            serializer = OrderItemSerializer(order.items.all(), many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as err:
            return Response({'error': err})
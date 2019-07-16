from django.contrib.auth.models import User
from .models import ProductModel,RatingModel
from .serializers import ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND,HTTP_200_OK
from rest_framework.response import Response

# singup
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):

	dictV = {}
	username = request.data.get("username")
	password = request.data.get("password")
	confirm_password = request.data.get("conf_password")

	if username is None or password is None or confirm_password is None:
		dictV['message'] = 'Username or passwords or confirm password is required'
		dictV['status'] = HTTP_400_BAD_REQUEST

	elif password != confirm_password:
		dictV['message'] = 'passwords did not matched'
		dictV['status'] = HTTP_400_BAD_REQUEST

	else:
		try:
			if username and password and password == confirm_password:
				user = User.objects.create(username = username)
				user.set_password(password)
				user.save()
				dictV['message'] = 'You have Successfull registered'
				dictV['status'] = HTTP_200_OK

		except Exception as e:
			dictV['message'] = 'User with same username already Exist'
			dictV['status'] = HTTP_400_BAD_REQUEST

	return Response(dictV)

#login
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):

	dictV = {}
	username = request.data.get("username")
	password = request.data.get("password")

	if username is None or password is None:
		dictV['message'] = 'Username and password is required'
		dictV['status'] = HTTP_400_BAD_REQUEST

	else:
		user = authenticate(username=username, password=password)
		if not user:
			dictV['message'] = 'Invalid credentials'
			dictV['status'] = HTTP_404_NOT_FOUND
		else:
			token, _ = Token.objects.get_or_create(user=user)
			dictV['status'] = HTTP_200_OK
			dictV['message'] = 'Login successfull'
			dictV['token'] = token.key

	return Response(dictV)

#get product list
@csrf_exempt
@api_view(["GET"])
def product(request):

	dictV = {}
	product = ProductModel.objects.all()
	serializer = ProductSerializer(product, many = True)
	if serializer.data:
		dictV['message'] = 'Products found'
		dictV['product'] = serializer.data
	else:
		dictV['product'] = []
		dictV['message'] = 'No products found'
	dictV['status'] = HTTP_200_OK
	return Response(dictV)

#give a rating to a product
@csrf_exempt
@api_view(["POST"])
def rateproduct(request):

	dictV = {}
	product_id = request.data.get("product_id")
	rating = request.data.get("rating")
	user = request.user

	if product_id and rating:
		try:
			product = RatingModel.objects.get(user = user, product_id = product_id)
			dictV['message'] = 'You have already rated this product'

		except RatingModel.DoesNotExist:
			product = RatingModel.objects.create(
				user = user,product_id = product_id,rating= rating
				)
			dictV['message'] = 'You have successfull rated this product'
		dictV['status'] = HTTP_200_OK

	else:
		if product_id is None:
			dictV['message'] = 'Product Id is required'
		else:
			dictV['message'] = 'Rating is required'
			dictV['status'] = HTTP_400_BAD_REQUEST

	return Response(dictV)






	


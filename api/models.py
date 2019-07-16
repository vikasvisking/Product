from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProductModel(models.Model):

	name = models.CharField(max_length = 50)
	price = models.FloatField()

	def __str__(self):
		return self.name + " : " + str(self.price)

class RatingModel(models.Model):

	product = models.ForeignKey(ProductModel, on_delete = models.CASCADE)
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	rating = models.FloatField()

	def __str__(self):
		return self.user.username + ' has given ' + str(self.rating) + ' rating to ' + self.product.name


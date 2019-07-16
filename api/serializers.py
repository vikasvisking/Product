from rest_framework import serializers
from .models import ProductModel, RatingModel

class ProductSerializer(serializers.ModelSerializer):
	rating = serializers.SerializerMethodField()

	class Meta:
		model = ProductModel
		fields = '__all__'

	def get_rating(self,obj):

		# assuming that max rating can be 5.
		rate = RatingModel.objects.filter(product = obj)
		if rate:
			one = RatingModel.objects.filter(product = obj, rating = 1)
			rate_one = sum([rat.rating for rat in one])

			two = RatingModel.objects.filter(product = obj, rating = 2)
			rate_two = sum([rat.rating for rat in two])

			three = RatingModel.objects.filter(product = obj, rating = 3)
			rate_three = sum([rat.rating for rat in three])

			four = RatingModel.objects.filter(product = obj, rating = 4)
			rate_four = sum([rat.rating for rat in four])

			five = RatingModel.objects.filter(product = obj, rating = 5)
			rate_five = sum([rat.rating for rat in five])

			sum_rate = rate_one + rate_two + rate_three + rate_four + rate_five
			if sum_rate != 0:
				avg_rating = (1 * rate_one + 2 * rate_two + 3 * rate_three + 4 * rate_four + 5 * rate_five) / sum_rate

			final_rat = format(avg_rating, '.2f')
		else:
			final_rat = 'No ratings yet'
		return final_rat


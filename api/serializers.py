from rest_framework import serializers
from app.models import StockInfo, StockCompany, PredictedStock




class PredictedSerializer(serializers.ModelSerializer):

	
	class Meta:
		model = PredictedStock
		fields = ('company', 'priceday1', 'priceday2', 'priceday3')



class TrendSerializer(serializers.ModelSerializer):

	company_name = serializers.CharField(source='company.company_name')
	companyfullname = serializers.CharField(source='company.companyfullname')

	class Meta:
		model = PredictedStock
		fields = ('company_name', 'companyfullname')



class StockSerializer(serializers.ModelSerializer):

	class Meta:
		model = StockInfo
		fields = ('companyprice', 'datetimecollect')

	def to_representation(self, instance):
		representation = super(StockSerializer, self).to_representation(instance)
		representation['datetimecollect'] = instance.datetimecollect.strftime("%b %d %Y")
		return representation


class ChartSerializer(serializers.ModelSerializer):

	companys = StockSerializer(many=True, read_only=True)

	class Meta:

		model = StockCompany
		#fields = ('info_id', 'companyprice', 'datetimecollect')
		fields = ('company_id', 'companys')


	#def to_representation(self, instance):
	#	representation = super(ChartSerializer, self).to_representation(instance)
	#	representation['datetimecollect'] = instance.datetimecollect.strftime("%b %d %Y")
	#	return representation
	



class TableSerializer(serializers.ModelSerializer):

	#stocks = serializers.StringRelatedField(many=True)

	company_name = serializers.CharField(source='company.company_name')
	company_id = serializers.IntegerField(source='company.company_id')
	company_categories = serializers.CharField(source='company.company_categories')

	class Meta:
		model = StockInfo
		fields = ('company_name', 'company_id', 'company_categories','companyprice', 'companyvolume', 'companyeps', 'companydps', 'companynta', 'companype', 'companydy', 'companyroe', 'companyptbv', 'companymcap')
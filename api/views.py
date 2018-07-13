from django.shortcuts import render
from django.http import HttpResponse
from django import template
from app.models import StockInfo, StockCompany, PredictedStock
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from .serializers import ChartSerializer, TableSerializer, PredictedSerializer, TrendSerializer
from django.utils import timezone
from django.db.models import Q, Min, Max
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils.safestring import mark_safe
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import simplejson as json
from datetime import date, timedelta
import datetime

class ChartData(viewsets.ModelViewSet):

	queryset = StockCompany.objects.all()

	serializer_class = ChartSerializer

	
	#queryset = StockCompany.objects.get(company_name="SCOMNET").companys.all()
	#stocks = StockInfo.objects.all().filter(company_code="0001")
	def list(self, request):
		queryset = self.get_queryset()
		serializer = ChartSerializer(queryset, many=True)
		return Response(serializer.data)
	

	#serializer = ChartSerializer(stocks, many=True)	

	#return Response(serializer.data)


class PredictedData(viewsets.ModelViewSet):

	queryset = PredictedStock.objects.all()


	serializer_class = PredictedSerializer


class UptrendData(APIView):

	def get(self, request):

		#stocks = StockCompany.objects.all()
		queryset = PredictedStock.objects.filter(stock_trend__contains='uptrend')
		serializer = TrendSerializer(queryset, many=True)

		return Response(serializer.data)
		


class DowntrendData(APIView):

	def get(self, request):

		queryset = PredictedStock.objects.filter(stock_trend__contains='downtrend')
		serializer = TrendSerializer(queryset, many=True)

		return Response(serializer.data)



class TableData(APIView):
	def post(self,request,*args,**kwargs):
				
		#declaring/getting values----------------------------
		renderer_classes = [TemplateHTMLRenderer]
		template_name = 'stock_market.html'
		
		largestVal = StockInfo.objects.aggregate(Max('companymcap'))
		print(largestVal.get('companymcap__max'))
		mcapRange = largestVal.get('companymcap__max') / 4
				
		
		largestPrice = StockInfo.objects.aggregate(Max('companyprice'))
		
		smallestPE = StockInfo.objects.aggregate(Min('companype'))
		largestPE = StockInfo.objects.aggregate(Max('companype'))
		peGap = (largestPE.get('companype__max') - smallestPE.get('companype__min')) / 3

		smallestEPS = StockInfo.objects.aggregate(Min('companyeps'))
		largestEPS = StockInfo.objects.aggregate(Max('companyeps'))
		EPSGap = (largestEPS.get('companyeps__max') - smallestEPS.get('companyeps__min')) / 3

		yesterday = datetime.datetime.now() - timedelta(1)
		today = datetime.datetime.now()
		#----end--dec/get values------------------------------




		
		#getting the values for the starting and end range for companymcap to be filtered
		endRange = request.POST.get('mcap')
		if endRange is None:
			endRange = largestVal.get('companymcap__max')
			startRange = 0
		else:
			endRange = float(endRange) * mcapRange
			startRange = endRange - mcapRange
		#--end-----------------------------------------------------------------------------




			
		
		#getting the values for what company price to filter----------------------------
		end_Price_Range = request.POST['sp']
		if "0" in end_Price_Range:
			end_Price_Range = largestPrice.get('companyprice__max')
			start_Price_Range = 0
		elif "1" in end_Price_Range:
			end_Price_Range = 1
			start_Price_Range = 0
		else:
			end_Price_Range = largestPrice.get('companyprice__max')
			start_Price_Range = 1
		#--end----------------------------------------------------------------------------




			
		print(" endPriceRange -- >" , end_Price_Range , " startPriceRange -- >", start_Price_Range)
		#getting the values for what company PE to filter---------------------------------
		end_PE_Range = request.POST['pe']
		if "0" in end_PE_Range:
			end_PE_Range = largestPE.get('companype__max')
			start_PE_Range = smallestPE.get('companype__min')
		elif "1" in end_PE_Range:
			end_PE_Range = (peGap * int(end_PE_Range)) + smallestPE.get('companype__min')
			start_PE_Range = smallestPE.get('companype__min') - peGap
		elif "2" in end_PE_Range:
			end_PE_Range = (peGap * int(end_PE_Range)) + smallestPE.get('companype__min')
			start_PE_Range = end_PE_Range - peGap
		else:
			end_PE_Range = (peGap * 3) + smallestPE.get('companype__min')
			start_PE_Range = end_PE_Range - peGap
		#--end----------------------------------------------------------------------------
		print(start_PE_Range, " " , end_PE_Range)




			
		#getting the values for what company EPS to filter---------------------------------
		end_EPS_Range = request.POST['eps']
		if "0" in end_EPS_Range:
			end_EPS_Range = largestEPS.get('companyeps__max')
			start_EPS_Range = smallestEPS.get('companyeps__min')
		elif "1" in end_EPS_Range:
			end_EPS_Range = (EPSGap * int(end_EPS_Range)) + smallestEPS.get('companyeps__min')
			start_EPS_Range = smallestEPS.get('companyeps__min') - EPSGap
		elif "2" in end_EPS_Range:
			end_EPS_Range = (EPSGap * int(end_EPS_Range)) + smallestEPS.get('companyeps__min')
			start_EPS_Range = end_EPS_Range - EPSGap
		else:
			end_EPS_Range = (EPSGap * 3) + smallestEPS.get('companyeps__min')
			start_EPS_Range = end_EPS_Range - EPSGap
		#--end----------------------------------------------------------------------------
		print(start_EPS_Range, " " , end_EPS_Range)

			

		#getting the values for which category to filter---------------------------------
		sector = request.POST['cat']
		if "All" in sector:
			sector = "%"
			stocks =  StockInfo.objects.filter(Q(datetimecollect__range=(yesterday,today)),Q(companyeps__range=(start_EPS_Range,end_EPS_Range)),Q(companype__range=(start_PE_Range,end_PE_Range)),Q(companyprice__range=(start_Price_Range,end_Price_Range)),Q(companymcap__range=(startRange,endRange)))
		else:
			sector = request.POST['cat']
			stocks =  StockInfo.objects.filter(Q(datetimecollect__range=(yesterday,today)),Q(company__company_categories__contains = sector),Q(companyeps__range=(start_EPS_Range,end_EPS_Range)),Q(companype__range=(start_PE_Range,end_PE_Range)),Q(companyprice__range=(start_Price_Range,end_Price_Range)),Q(companymcap__range=(startRange,endRange)))
		#--end---------------------------------------------------------------------------


		#datetimecollect__range=(yesterday,today)
		#stocks = StockInfo.objects.filter(datetimecollect__contains=datetime.date(2018, 3, 13))


		serializer = TableSerializer(stocks,many=True)
		testing = json.dumps(list(serializer.data))
		context = {'data':testing,}
		return render(request,'app/stock_market.html',context)
#end------------------------------------------------------------------------------------------------

	def get(self, request):

		yesterday = datetime.datetime.now() - timedelta(1)
		today = datetime.datetime.now()

		#stocks = StockCompany.objects.all()
		stocks = StockInfo.objects.filter(datetimecollect__range=(yesterday,today))
		serializer = TableSerializer(stocks, many=True)
		testing = json.dumps(list(serializer.data))
		context = {'data':testing,}
		

		

		return render(request,'app/stock_market.html',context)

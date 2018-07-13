import datetime
from datetime import timedelta

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import Http404
from app.models import StockInfo, StockCompany, Portfolio, PredictedStock
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min

from rest_framework.views import APIView
from rest_framework.response import Response


from .services import get_stocks


from app.forms import PortfolioForm


import numpy as np
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def predict_price(dates,prices,x):


    linear_mod = linear_model.LinearRegression() #defining the linear regression model
    dates = np.reshape(dates,(len(dates),1)) # converting to matrix of n X 1
    prices = np.reshape(prices,(len(prices),1))
    linear_mod.fit(dates,prices) #fitting the data points in the model
    predicted_price =linear_mod.predict(x)
    return predicted_price[0][0],linear_mod.coef_[0][0] ,linear_mod.intercept_[0]




class stockView(TemplateView):
	template_name = 'app/stock.html'
	

	def get(self, request):


		
		#stockInfo = StockInfo.objects.values('companyprice')
		#args = {'stockInfo': stockInfo}

		#stock_list = get_stocks()

		company_name = request.GET.get('q')

		try:
			stocks = StockCompany.objects.get(company_name = company_name).companys.all().latest('datetimecollect')

			day1 = stocks.datetimecollect + timedelta(days=1)
			day2 = stocks.datetimecollect + timedelta(days=2)
			day3 = stocks.datetimecollect + timedelta(days=3)

			day1 = day1.strftime("%b %d %Y")
			day2 = day2.strftime("%b %d %Y")
			day3 = day3.strftime("%b %d %Y")

		except StockCompany.DoesNotExist:
			raise Http404("No company matches the company name.")

		#stocks = StockInfo.objects.filter(company_code = company_code).latest('datetimecollect')

		
		predictedStock = PredictedStock.objects.get(company__company_name = company_name)





		args = {'stocks': stocks, 'predictedStock': predictedStock, 'day1':day1, 'day2':day2, 'day3':day3 }

		#stocks = StockCompany.objects.filter(company_name = company_name).stockinfo_set
		

		return render(request, self.template_name, args)




#def get_data(request, *args, **kwargs):

#	results = StockInfo.objects.values('companyprice', 'datetimecollect')

#	return JsonResponse({'result': list(results)})



@login_required()
def home(request):

	if request.method == 'GET':
		portfolio = Portfolio.objects.filter(owner=request.user)[:5]

		uptrendStock = PredictedStock.objects.filter(stock_trend__contains= 'uptrend')[:5]

		downtrendStock = PredictedStock.objects.filter(stock_trend__contains= 'downtrend')[:5]

		highestCof = PredictedStock.objects.aggregate(Max('coefficient'))

		lowestCof = PredictedStock.objects.aggregate(Min('coefficient'))
		
		data = highestCof.get("coefficient__max")

		data2 = lowestCof.get("coefficient__min")
		

		bestUptrend = PredictedStock.objects.get(coefficient__contains = data)

		worstDowntrend = PredictedStock.objects.get(coefficient__contains = data2)


		#Get 3 days of future date of current stock and return to the home page
		stocks = StockCompany.objects.get(company_name = 'SCOMNET').companys.all().latest('datetimecollect')

		day1 = stocks.datetimecollect + timedelta(days=1)
		day2 = stocks.datetimecollect + timedelta(days=2)
		day3 = stocks.datetimecollect + timedelta(days=3)

		day1 = day1.strftime("%b %d %Y")
		day2 = day2.strftime("%b %d %Y")
		day3 = day3.strftime("%b %d %Y")

		args = {'portfolio': portfolio, 'uptrendStock': uptrendStock, 'downtrendStock': downtrendStock, 'bestUptrend': bestUptrend, 'worstDowntrend': worstDowntrend, 'day1':day1, 'day2':day2, 'day3': day3}

		return render(request, 'app/home_new.html', args)



class stockMarketView(TemplateView):
	
	template_name = 'app/stock_market.html'


def stockMarketView(request):

	if request.method == 'GET':
		return redirect('tableData')



def stockAsJson(request):


	test = StockCompany.objects.all()

	#stocks = StockInfo.objects.filter(company = test.company_id)

	

	json = serializers.serialize('json', test)

	

	return HttpResponse(json, content_type='application/json')


@login_required()
def prediction(request):

	if request.method == 'GET':


		predictedStock = PredictedStock.objects.all();



		args = {'predictedStock':predictedStock}

		return render(request, 'app/prediction.html', args)
	


class PortfolioView(TemplateView):

	template_name = 'app/portfolio.html'


	def get(self, request):

		form = PortfolioForm()

		#Getting data from portfolio
		portfolio = Portfolio.objects.filter(owner=request.user)

		args = {'form':form, 'portfolio':portfolio}

		return render(request, self.template_name, args)


	def post(self, request):

		form_data = PortfolioForm(request.POST)
		form = PortfolioForm()

		#Getting data from form
		if form_data.is_valid():
			symbol = form_data.cleaned_data['symbols']

			stockinfo = StockCompany.objects.get(company_name=symbol).companys.all().latest('datetimecollect')

			instance = form.save(commit=False)


			instance.porfolio_info = stockinfo
			instance.owner = request.user
			instance.portfolio_info = stockinfo
			instance.symbols = symbol

			instance.save()


		#Getting data from portfolio
		portfolio = Portfolio.objects.filter(owner=request.user)

		args = {'form': form, 'portfolio':portfolio}

		return render(request, self.template_name, args)



@login_required()
def delete_symbol(request):

	if request.method == 'POST':

		form_data = PortfolioForm(request.POST)
		form = PortfolioForm()

		#Getting data from form
		if form_data.is_valid():
			symbol = form_data.cleaned_data['symbols']


			try:
				portfolio = Portfolio.objects.filter(owner = request.user, symbols = symbol)

			except Portfolio.DoesNotExist:
				raise Http404("No symbol exists.")
	
			
			portfolio.delete()
			return redirect('portfolio')



		#Getting data from portfolio
		#portfolio = Portfolio.objects.filter(owner=request.user)

		#args = {'form': form, 'portfolio':portfolio}

		
		#return render(request, 'app/portfolio.html', args)

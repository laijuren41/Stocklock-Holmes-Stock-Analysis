from django import forms
from app.models import Portfolio


class PortfolioForm(forms.ModelForm):

	class Meta:
		model = Portfolio
		fields = {'symbols'}
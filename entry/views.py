from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout


def log_out(request):

	if request.method == 'POST':
		logout(request)
		return redirect('login')


def log_in(request):

	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)

		if form.is_valid():
			#log in the user
			user = form.get_user()

			login(request, user)

			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('home')


	else:
		form = AuthenticationForm()
	

	return render(request, 'entry/log_in.html', {'form':form})


def register(request):
	

	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			user = form.save()
			
			login(request, user)
			return redirect('home')

	else:
		form = UserCreationForm()
	
	return render(request, 'entry/register.html', {'form': form})





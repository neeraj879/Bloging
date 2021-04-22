from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm,UserUpdate,ProfileUpdate
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			send_mail(
				'Welcome !',
				'Good to see you here !'+str(form.cleaned_data.get('username')),
				'neerajmaurya879@gmail.com',
				[str(form.cleaned_data.get('email'))],
				fail_silently=False
			)
			username=form.cleaned_data.get('username')
			messages.success(request,f'Account created for {username}!')
			return redirect('profile')
	else:
		form = RegisterForm()
	return render(request,'users/register.html',{'form':form})
@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdate(request.POST, instance=request.user)
		p_form = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('profile')
	else:
		u_form = UserUpdate()
		p_form = ProfileUpdate()
	context={'u_form':u_form,'p_form':p_form}
	return render(request,'users/profile.html',context)
	
		
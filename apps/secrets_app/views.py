# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import UserManager, User, SecretManager, Secret
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Count

# Create your views here.
def index(request):
	if 'user' in request.session:
		return render(request, 'secrets_app/main.html')
	else:
		return render(request, 'secrets_app/index.html')

def login(request):
	if request.method=='POST':
		login = User.objects.login(request.POST.copy())
		if isinstance(login, list):
			for item in login:
				messages.error(request, item)
			return redirect(reverse('index'))
		else:
			request.session['user'] = login.id
			return redirect(reverse('main'))
	else:
		return redirect(reverse('index'))

def register(request):
	if request.method=='POST':
		register = User.objects.register(request.POST.copy())
		if isinstance(register, list):
			for item in register:
				messages.error(request, item)
			return redirect(reverse('index'))
		else:
			request.session['user'] = register.id
			return redirect(reverse('main'))
	else:
		return redirect(reverse('index'))

def main(request):
	if 'user' in request.session:
		user = User.objects.get(id=request.session['user'])
		secrets = Secret.objects.all().order_by('-created_at')[:5]
		likes = Secret.objects.filter(likes__id=user.id)
		context = {
			'name':user.first_name+' '+user.last_name,
			'user':user.id,
			'secrets': secrets,
			'liked':likes
		}

		return render(request, 'secrets_app/main.html', context)
	else:
		messages.error(request, 'Log in or register first')
		return redirect(reverse('index'))

def logout(request):
	request.session.pop('user')
	return redirect(reverse('index'))

def popular(request):
	user = User.objects.get(id=request.session['user'])
	secrets = Secret.objects.all().annotate(num=Count('likes')).order_by('-num')
	likes = Secret.objects.filter(likes__id=user.id)
	context = {
		'user':user.id,
		'secrets':secrets,
		'liked':likes
	}
	return render(request, 'secrets_app/popular.html', context)

def secret(request):
	if request.method=='POST':
		new_post = Secret.objects.post(request.POST.copy())
		if isinstance(new_post, list):
			for item in new_post:
				messages.error(request, item)
		else:
			new_secret = Secret.objects.create(content=request.POST['secret_post'], secret_user=User.objects.get(id=request.session['user']))
	return redirect(reverse('main'))

def like(request,id):
	user = User.objects.get(id=request.session['user'])
	secret = Secret.objects.get(id=id)
	secret.likes.add(user)
	origin = request.META['HTTP_REFERER']
	page=origin.split('/')[3]
	return  redirect(reverse(page))

def delete(request,id):
	Secret.objects.get(id=id).delete()
	origin = request.META['HTTP_REFERER']
	page=origin.split('/')[3]
	return  redirect(reverse(page))

def my_likes(request):
	user = User.objects.get(id=request.session['user'])
	secrets = Secret.objects.filter(secret_user__id=user.id).order_by('-created_at') | Secret.objects.filter(likes__id=user.id).order_by('-created_at')
	likes = Secret.objects.filter(likes__id=user.id)
	context = {
		'user':user.id,
		'secrets':secrets,
		'liked':likes
	}
	return render(request, 'secrets_app/my_likes.html', context)

def my_unlikes(request):
	user = User.objects.get(id=request.session['user'])
	secrets = Secret.objects.exclude(secret_user__id=user.id).exclude(likes__id=user.id).order_by('-created_at')
	context = {
		'user':user.id,
		'secrets':secrets
	}
	return render(request,'secrets_app/my_unlikes.html',context)
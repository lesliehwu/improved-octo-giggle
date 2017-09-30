# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.db import connection, transaction
from django.contrib import messages

# Create your views here.

def index(request):
    if 'id' not in request.session:
        request.session['id'] = -1
    return render(request, 'index.html')

def register(request):
    errors = User.objects.reg_validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags = field)
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
        request.session['id'] = user.id
        return redirect('/success')

def login(request):
    errors = User.objects.log_validate(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags = field)
        return redirect('/')
    else:
        user = User.objects.get(email=request.session['email'])
        request.session['id'] = user.id
        return redirect('/success')

def success(request):
    context = {
            "user":User.objects.get(id=request.session['id'])
    }
    return render(request, 'success.html', context)

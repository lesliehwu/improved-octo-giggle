# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def reg_validate(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be at least 2 characters long'
        elif not post_data['first_name'].isalpha():
            errors['first_name'] = 'First name can only contain letters'
        
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be at least 2 characters long'
        elif not post_data['last_name'].isalpha():
            errors['last_name'] = 'Last name can only contain letters'

        if len(post_data['email']) < 0:
            errors['email'] = 'Email is required'
        elif not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = 'Email is invalid'
        elif len(self.filter(email=post_data['email'])) > 1:
            errors['email'] = 'Email is already registered'

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        if not post_data['password'] == post_data['confirm']:
            errors['confirm'] = 'Password fields do not match'

        return errors
    
    def log_validate(self, post_data):
        errors = {}
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = 'Email is invalid'
        elif len(self.filter(email=post_data['email'])):
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(),user.password.encode()):
                errors['password'] = 'Email and/or password is incorrect'
        return errors
        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

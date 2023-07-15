from django.db import models
import re

class UserManager(models.Manager):
  
  def user_validator(self, post_data):
    errors = {}
    if len(post_data['fname']) < 2: 
      errors['fname_error'] = "First name not long enough. Must be at least 2 characters."
    if len(post_data['lname']) < 2: 
      errors['lname_error'] = "Last name not long enough. Must be at least 2 characters."
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(post_data['email']):           
      errors['email_invalid_error'] = "Invalid email address!"
    if len(post_data['password']) < 8:
      errors['password_length_error'] = "Password is not long enough! Must be at least 8 characters."
    if post_data['password'] != post_data['confirm_password']: 
      errors['password_match_error'] = "Passwords have to match!"    
    return errors

  def registration_validator(self, post_data):
    errors = {}
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(post_data['email']):           
      errors['email_invalid_error'] = "Invalid email address!"
    return errors

class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.EmailField()
  password = models.CharField(max_length=300)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()


class ItemManager(models.Manager):
  def item_validator(self, post_data):
    errors = {}
    if len(post_data['item']) < 2: 
      errors['item_name_error'] = "Item must be 2 characters or longer!"
    return errors

class Item(models.Model):
  item = models.CharField(max_length=100)
  item_quantity = models.IntegerField()
  item_type = models.CharField(max_length=100)
  date_bought = models.CharField(max_length=100)
  date_listed = models.CharField(max_length=100)
  date_sold = models.CharField(max_length=100, default='0')
  price_paid = models.CharField(max_length=100)
  listing_price = models.CharField(max_length=100)
  gross_profit = models.CharField(max_length=100, default='0')
  selling_platform = models.CharField(max_length=100, default='0')
  shipping_fee = models.CharField(max_length=100, default='0')
  additional_fees = models.CharField(max_length=100, default='0')
  total_profit = models.CharField(max_length=100, default='0')
  item_sold = models.BooleanField(default=False)
  uploaded_by = models.ForeignKey(User, related_name="item_uploaded", on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = ItemManager()

class MileageManager(models.Manager):
  def mileage_validator(self, post_data):
    errors = {}
    if len(post_data['purpose']) < 5:
      errors['purpose_error'] = 'purpose length invalid'
    return errors


class Mileage(models.Model):
  travel_date = models.CharField(max_length=100)
  mileage = models.CharField(max_length=50)
  purpose = models.CharField(max_length=100)
  uploaded_by = models.ForeignKey(User, related_name="mileage_uploaded", on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = MileageManager()
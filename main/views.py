from django.shortcuts import render, redirect, HttpResponse
from .models import Item, Mileage, User
from django.contrib import messages
import bcrypt
# Create your views here.

STRING_ZERO = '0'

def index(request):
  context = {
    'users' : User.objects.all(),
  }
  return render(request, 'index.html', context)

def register(request):
  errors = User.objects.user_validator(request.POST)
  if len(errors) > 0: 
    for msg in errors.values():
      messages.error(request, msg)
    return redirect('/')
  password = request.POST['password']
  hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  user = User.objects.create(
    first_name = request.POST['fname'],
    last_name = request.POST['lname'],
    email = request.POST['email'],
    password = hashed,
  )
  request.session['user_id'] = user.id
  return redirect('/dashboard')

def login(request):
  errors = User.objects.registration_validator(request.POST)
  if len(errors) > 0:
    for msg in errors.values():
      messages.error(request, msg)  
  user_login_email = User.objects.filter(email=request.POST['email'])
  if len(user_login_email) > 0:
    first_user = user_login_email[0]
    if bcrypt.checkpw(request.POST['password'].encode(), first_user.password.encode()):
      request.session['user_id'] = first_user.id
      return redirect('/dashboard')
  messages.error(request, "Email/Password Invalid!")
  return redirect('/')

def dashboard(request):
  if 'user_id' not in request.session:
    return redirect('/')
  context = {
    'user' : User.objects.get(id=request.session['user_id']), 
  }
  return render(request, 'dashboard.html', context)


def logout(request):
  del request.session['user_id']
  return redirect('/')

def view_inventory(request):
  if 'user_id' not in request.session:
    return redirect('/')
  context = {
    'user' : User.objects.get(id=request.session['user_id']),
    'items' : Item.objects.all(), 
  }
  return render(request, 'view_inventory.html', context)

def add_item_page(request):
  return render(request, 'add_item.html')

def create_item(request):
  # print(request.POST)
  errors = Item.objects.item_validator(request.POST)
  if len(errors) > 0:
    for msg in errors.values():
      messages.error(request, msg)
      return redirect('/add_item_page')

  date_bought = ''
  price_paid = ''
  if request.POST['item_type'] == 'Flip':
    date_bought = request.POST['date_bought']
    price_paid = request.POST['price_paid']
  else: 
    date_bought = '2000-01-01'
    price_paid = '0'
  Item.objects.create(
    item = request.POST['item'],
    item_quantity = request.POST['item_quantity'],
    item_type = request.POST['item_type'],
    date_bought = date_bought,
    date_listed = request.POST['date_listed'],
    price_paid = price_paid,
    selling_platform = request.POST['selling_platform'],
    uploaded_by = User.objects.get(id = request.session['user_id'])
  )
  return redirect('/dashboard')

def item_sold_form(request, item_id):
  context = {
    'user' : User.objects.get(id=request.session['user_id']),
    'item' : Item.objects.get(id = item_id)
  }
  return render(request, 'item_sold_form.html', context)

def complete_sell(request, item_id):
  item_sold = Item.objects.get(id = item_id)
  item_sold.date_sold = request.POST['date_sold']
  item_sold.gross_profit = request.POST['gross_profit']
  item_sold.shipping_fee = request.POST['shipping_fee']
  item_sold.additional_fees = request.POST['additional_fees']
  item_sold.item_sold = True
  item_sold.total_profit = round(float(item_sold.gross_profit) - float(item_sold.additional_fees) - float(item_sold.price_paid) - float(item_sold.shipping_fee), 2)
  item_sold.save()
  return redirect('/finance_page')

def finance_page(request):
  context = {
    'user' : User.objects.get(id = request.session['user_id']),
    'items' : Item.objects.all()
  }
  return render(request, 'finance_page.html', context)

def add_to_backlog(request):
  context = {
    'user' : User.objects.get(id = request.session['user_id']),
    'items' : Item.objects.all()
  }
  return render(request, 'backlog_form.html', context)

def mileage_sheet(request):
  context = {
    'user' : User.objects.get(id = request.session['user_id']),
    'mileages' : Mileage.objects.all()
  }
  return render(request, 'mileage_sheet.html', context)

def add_mileage_sheet(request):
  return render(request, 'add_mileage.html')

def process_mileage(request):
  errors = Mileage.objects.mileage_validator(request.POST)
  if len(errors) > 0:
    for msg in errors.values():
      messages.error(request, msg)
    return redirect('/add_mileage')

  Mileage.objects.create(
    travel_date = request.POST['travel_date'],
    mileage = request.POST['mileage'],
    purpose = request.POST['purpose'],
    uploaded_by = User.objects.get(id = request.session['user_id'])
  )  
  return redirect('/mileage_sheet')
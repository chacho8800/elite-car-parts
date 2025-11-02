from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Part, Car
from django.views.generic import CreateView, DeleteView



# Create your views here.
class Login(LoginView):
    template_name = 'login.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)
            return redirect('home')
        else: 
            error_message = "Invalid sign up - try again"
    
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message' : error_message}
    return render(request, 'signup.html', context)

def account(request):
    return render(request, "account.html")

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request,"about.html")

@login_required
def part_index(request):
    parts = Part.objects.filter(owner=request.user)
    return render(request, "parts/index.html", {"parts": parts})

@login_required
def part_detail(request, part_id):
    part = Part.objects.get(id=part_id)
    return render(request, "parts/detail.html", {"part" : part})

@login_required
def add_to_cart(request, part_id):
    part = Part.objects.get(id=part_id)

    cart = request.session.get('cart', {})

    if str(part_id) in cart: 
        cart[str(part_id)] += 1
    else:
        cart[str(part_id)] = 1

    request.session['cart'] = cart
    return redirect('part-index') 

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    parts = Part.objects.filter(id__in=cart.keys())
    cart_items = []

    for part in parts:
        cart_items.append({
            'part': part,
            'quantity': cart[str(part.id)],
        })

    return render(request, 'parts/cart.html', {'cart_items': cart_items})

class CartDelete(LoginRequiredMixin, DeleteView):

    def get(self, request, part_id):
        cart = request.session.get('cart', {})
        part_id_str = str(part_id)
        if part_id_str in cart:
            cart[part_id_str] -= 1 
            if cart[part_id_str] <= 0:
                del cart[part_id_str]
            request.session['cart'] = cart  
        return redirect('view-cart')




    
    
    
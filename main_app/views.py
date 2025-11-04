from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm
from .models import Part, Car, Review
from django.views.generic import CreateView, DeleteView, UpdateView



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

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request,"about.html")

@login_required
def account(request):
    parts = Part.objects.filter(owner=request.user)
    cars = Car.objects.filter(owner=request.user)
    return render(request, "account.html", {"parts" : parts, "cars" : cars})

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

@login_required
def search_part(request):
    query = request.GET.get("q", "")
    parts = Part.objects.all()

    if request.user.is_authenticated:
        parts = parts.filter(owner=request.user)

    if query:
        parts = parts.filter(name__icontains=query)

    context = {
        "query": query,
        "parts": parts,
    }
    return render(request, "parts/search_results.html", context)


@login_required
def add_review(request, part_id):
    part = Part.objects.get(id=part_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        # Prevent empty reviews
        if rating and comment:

             # Create the Review object
            Review.objects.create(
                part=part,
                user=request.user,
                rating=rating,
                comment=comment
            )
            return redirect("part-detail", part_id=part.id)

    return render(request, "parts/detail.html", {"part": part})


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

class CarDelete(LoginRequiredMixin, DeleteView):
    model = Car
    success_url ='/account/'

class CarUpdate(LoginRequiredMixin,UpdateView):
    model = Car
    fields = ['make', 'model', 'year']
    success_url = '/account/'

class CarCreate(LoginRequiredMixin,CreateView):
    model = Car
    fields = ['make', 'model', 'year']
    success_url = '/account/'

    def form_valid(self, form):
        form.instance.owner = self.request.user  
        return super().form_valid(form)
    

def parts_by_category(request, category=None):
    parts = Part.objects.all()
    if category:
        parts = parts.filter(category__iexact=category)
    return render(request, "parts/index.html", {"parts": parts, "filter_type": "Category", "filter_value": category})


def parts_by_make(request, make):
    parts = Part.objects.filter(car__make__iexact=make)
    return render(request, "parts/index.html", {"parts": parts, "filter_type": "Make", "filter_value": make})


def parts_by_model(request, model):
    parts = Part.objects.filter(car__model__iexact=model)
    return render(request, "parts/index.html", {"parts": parts, "filter_type": "Model", "filter_value": model})


def parts_by_price(request):
    parts = Part.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        parts = parts.filter(price__gte=min_price)
    if max_price:
        parts = parts.filter(price__lte=max_price)

    filter_value = f"${min_price or 0} - ${max_price or '∞'}"

    return render(request, 'parts/index.html', {
        'parts': parts,
        'filter_type': 'Price',
        'filter_value': filter_value
    })
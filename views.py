from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .forms import CustomUserCreationForm
from .models import Item

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Username or password is incorrect'})
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html', {'user_info': request.user})

@login_required
def adjust_amount(request, item_id, action):
    item = get_object_or_404(Item, id=item_id)
    if action == 'add':
        item.amount += 1
    elif action == 'subtract':
        item.amount -= 1
        if item.amount < 0:
            item.amount = 0
    item.save()
    return redirect('home')

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')

class AjaxCreateItem(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        user = request.user

        item = Item.objects.create(name=name, amount=amount, user=user)
        item.save()
        return JsonResponse({'status': 'ok'}, status=201)

@login_required
def get_items(request):
    items = list(Item.objects.filter(user=request.user).values())
    return JsonResponse({'items': items}, safe=False)

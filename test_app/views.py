from urllib import request

from django.contrib import auth
from django.shortcuts import render, redirect

# Create your views here.

from test_app.models import Category, Product, Review
from forms import *


def get_all_posts(request):
    product = Product.objects.all()

    data = {
        'products': product,
    }

    for i in range(len(data['products'])):
        col = Review.objects.filter(product_id=data['products'][i].id)
        data['products'][i].col = col.count()

    return render(request, 'index.html', context=data)


def get_one_product(request, id):
    product = Product.objects.get(id=id)
    review = Review.objects.filter(product_id=id)

    data = {
        'product': product,
        'review': review,
    }

    return render(request, 'add1.html', context=data)


def add_category(request):

    if request.method == "POST":
        categoryForm = CourseForm(data=request.POST)

        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('/posts/')
        else:
            return render(request, 'add.html', context={'forms': categoryForm})

    data = {
     'forms': CourseForm
    }

    return render(request, 'add.html', context=data)


def main_page(request):
    data = {
        'username': auth.get_user(request).username
    }
    return render(request, 'main.html', context=data)



def register(request):
    if request.method=='POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            print('POST запрос без ошибок')
            return redirect('/admin/')
        else:
            print('POST запрос с ошибкой')
            return render(request, 'register.html', context={'form': form})
    data = {
        'form': UserCreationForm(),
        'username': auth.get_user(request).username
    }
    print('GET запрос ')
    return render(request, 'register.html', context=data)


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
            )
            if user is not None:
                auth.login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', context={'form': form})
    data = {
        'form': LoginForm(),
        'username': auth.get_user(request).username
    }
    return render(request, 'login.html', context=data)


def logout(request):
    auth.logout(request)
    return redirect('/')

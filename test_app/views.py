from urllib import request

from django.shortcuts import render

# Create your views here.

from test_app.models import Category, Product


def get_all_posts():
    category = Category.objects.all()
    product = Product.objects.all()
    data = {
        'category': category,
        'product': product,
    }

    return render(request, 'index.html', context=data)

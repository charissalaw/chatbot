from django.shortcuts import render
from django.template.loader import get_template
from django.template import Context
from ninja import Router
from .models import Product, ProductCategory


router = Router()

@router.get('/products')
def list_products(request):
    return [
        {"id": p.id, "title": p.title}
        for p in Product.objects.all()
    ]

@router.get('/products/{product_id}')
def product(request, product_id: int):
    product = Product.objects.get(id=product_id)
    return render(request, 'product.html',
    {
        "title": product.title,
        "image": product.image_filename,
        "description": product.description
    })

@router.get('/category/{category_slug}')
def category(request, category_slug: str):
    category = ProductCategory.objects.get(slug=category_slug)
    return render(request, 'product.html',
    {
        "title": category.name,
        "image": category.image_filename,
    })

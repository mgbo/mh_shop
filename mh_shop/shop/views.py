

from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	all_products = Product.objects.filter(available=True)


	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		all_products = all_products.filter(category=category)
		
	paginator = Paginator(all_products, 9)
	page = request.GET.get('page')

	try:
		products = paginator.page(page)

	except PageNotAnInteger:
		products = paginator.page(1)

	except EmptyPage:
		products = paginator.page(paginator.num_pages)


	return render(request,'shop/product/list.html', 
													{'category': category, 
													'categories': categories, 
													'products':products,
													'page':page})

def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	cart_product_form = CartAddProductForm()
	return render(request,'shop/product/detail.html', 
													{'product': product,
													'cart_product_form':cart_product_form})


























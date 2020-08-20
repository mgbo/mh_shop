

from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)


	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
		
	paginator = Paginator(products, 3)
	page = request.GET.get('page')

	try:
		p_l = paginator.page(page)

	except PageNotAnInteger:
		p_l = paginator.page(1)

	except EmptyPage:
		p_l = paginator.page(paginator.num_pages)


	return render(request,'shop/product/list.html', 
													{'category': category, 
													'categories': categories, 
													'products':products,
													'page':page,
													 'p_l': p_l})

def product_detail(request, id, slug):
	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	return render(request,'shop/product/detail.html', 
													{'product': product})
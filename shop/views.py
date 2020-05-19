from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Like
from .forms import ProductForm, ProductUpdateForm
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required()
def product(request, slug=None):
    category = None
    

    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(title__icontains=search_query)
    else:
        products = Product.objects.all()
    user = request.user

    paginator = Paginator(products, 10)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    is_paginated = page.has_other_pages()
    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    likes = Product.objects.filter(liked=request.user)
    categories = Category.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        page = Product.objects.filter(category=category)
    
    context = {
        'category': category,
        'categories': categories,  
        'products': page, 
        'likes': likes, 
        'user': user, 
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        }
    return render(request, 'products/index.html', context)



def detail(request, id):
    product = get_object_or_404(Product, id=id)
    context = {'product': product}
    return render(request, 'products/detail.html', context)




def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.slug = product.title
            product.save()
            return redirect('/')
    else:
        product_form = ProductForm()
    context = {'product_form': product_form}
    return render(request, 'products/create.html', context)


def product_update(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductUpdateForm(instance=product)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_form = form.save(commit=False)
            product_form.slug = product_form.title
            product_form.save()
            return redirect('/')
    else:
        form = ProductUpdateForm()
    context = {'form': form}
    return render(request, 'products/update.html', context)


def product_delete(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('/')
    context = {'product': product}
    return render(request, 'products/delete.html', context)


def like_post(request):
    user = request.user
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    if request.method == 'POST':

        if user in product_obj.liked.all():
            product_obj.liked.remove(user)
        else:
            product_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, product_id=product_id)

        if not created:
            if like.value == 'like':
                like.value = 'unlike'
            else:
                like.value = 'like'
        like.save()
    return redirect('product')
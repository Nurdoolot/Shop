from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm, ProductUpdateForm
from django.shortcuts import redirect



def product(request, slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products =    products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'products/index.html', context)



def detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
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

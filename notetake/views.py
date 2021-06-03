from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from .forms import CategoryForm, ProductForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives


@login_required
def categories_list(request):
	categories = Category.objects.all().order_by('-created_on')
	return render(request, 'notetake/category_list.html',{'categories':categories})


@login_required
def category_detail(request,pk):
	category = get_object_or_404(Category, pk=pk)
	products = Product.objects.filter(category=pk).order_by('-created_on')
	return render(request, 'notetake/category_detail.html', {'category': category,'products':products})


@login_required
def category_new(request):
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			category = form.save(commit=False)
			category.user = request.user
			category.save()
			return redirect('category_detail', pk=category.pk)
	else:
		form = CategoryForm()
	return render(request, 'notetake/category_edit.html', {'form': form})


@login_required
def category_edit(request, pk):
	category = get_object_or_404(Category, pk=pk)
	if request.method == "POST":
		form = CategoryForm(request.POST, instance=category)
		if form.is_valid():
			category = form.save(commit=False)
			category.user = request.user
			category.save()
			return redirect('category_detail', pk=category.pk)
	else:
		form = CategoryForm(instance=category)
	return render(request, 'notetake/category_edit.html', {'form': form})


@login_required
def category_delete(request, pk):
	category = get_object_or_404(Category, pk=pk)
	category.delete()
	return redirect('categories_list')


@login_required
def product_new(request):
	if request.method == "POST":
		form = ProductForm(request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			users = User.objects.filter(is_superuser=True).values('email')
			if users:
				to = []
				for i in users:
					to.append(i['email'])
				subject, from_email, to = 'Updation', 'qcaredocs.test@gmail.com', to
				msg = EmailMultiAlternatives(subject, 'Hello {0}, {1} created successfully'.format(product.user.username,product.title), from_email, to)
				msg.send()
			return redirect('category_detail', pk=product.category.pk)
	else:
		form = ProductForm()
	return render(request, 'notetake/product_edit.html', {'form': form})


@login_required
def product_edit(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == "POST":
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.save()
			return redirect('category_detail', pk=product.category.pk)
	else:
		form = ProductForm(instance=product)
	return render(request, 'notetake/category_edit.html', {'form': form})


@login_required
def product_delete(request, id, pk):
	product = get_object_or_404(Product, pk=pk)
	product.delete()
	return redirect('category_detail', pk=id)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('categories_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})
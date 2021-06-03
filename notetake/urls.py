from django.urls import path
from . import views

urlpatterns = [
	path('dashboard/',views.categories_list, name="categories_list"),
	path('category/<int:pk>/', views.category_detail, name='category_detail'),
	path('category/new/', views.category_new, name='category_new'),
	path('category/<int:pk>/edit', views.category_edit, name='category_edit'),
	path('category/<pk>/delete', views.category_delete, name='category_delete'),


	path('product/new/', views.product_new, name='product_new'),
	path('product/<int:pk>/edit', views.product_edit, name='product_edit'),
	path('note/<int:id>/product/<pk>/delete', views.product_delete, name='product_delete'),

	path('register', views.register, name='register'),
]

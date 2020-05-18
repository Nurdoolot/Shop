from django.urls import path
from .views import product, detail, product_create, product_delete, product_update, like_post


urlpatterns = [
    path('', product, name='product'),
    path('like/', like_post, name='like'),
    path('create/', product_create, name='create'),
    path('update/<int:pk>/', product_update, name='update'),
    path('delete/<int:pk>/', product_delete, name='delete'),
    path('<slug:slug>/', product, name='product_by_category'),
    path('<int:id>/<slug:slug>/', detail, name='detail'),
]
from django.contrib import admin
from django.urls import path
from store import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('user',views.user,name='user'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wish/<int:product_id>/', views.add_to_wish, name='add_to_wish'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('cart/',views.cart,name='cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_wish/<int:product_id>/', views.remove_wish, name='remove_wish'),
    path('orders',views.orders,name='orders'),
    path('search',views.search,name='search'),
]
urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

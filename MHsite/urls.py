"""MHsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from catalog import views
from catalog.views import CatalogListView, ItemDetailView, home_catalog
from django.contrib.auth import views as auth_views
from users import views as user_views
from contact.views import ContactView
from django.conf import settings
from django.conf.urls.static import static
from payments import views as payment_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.enter, name='enter'),
    path('home/', views.home, name='home'), #auth_views.LoginView.as_view(template_name='catalog/home.html'), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', ContactView, name='contact'),
    path('catalog/', CatalogListView.as_view(), name='catalog'),
    path('signup/', user_views.Register, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/complete', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('profile/', payment_views.ProfileView , name='profile'),
    path('profile/<slug:slug>', payment_views.ProfileOrderView, name='profile_orders'),
    path('detail/<int:pk>', views.ItemDetailView.as_view(), name='detail'),
    path('cart/', user_views.cart_home, name='cart_home'),
    path('update/', user_views.cart_update, name='cart_update'),
    path('catalog_preview/', home_catalog.as_view(), name='catalog_preview'),
    path('order/', payment_views.OrderCreateView.as_view(), name='create-order'),
    path('orderdetail/<slug:slug>', payment_views.OrderDetailView, name='CTT_order_detail'),
    path('orderdetail/<slug:slug>/edit', payment_views.OrdereditView.as_view(), name='CTT_order_edit'),
    path('orderfinish/<slug:slug>', payment_views.OrderFinal, name='order_finish'),
    path('charge/<slug:slug>', payment_views.charge , name='charge'),
    path('orderfinal/<slug:slug>', payment_views.OrderConfirmed, name='order_final'),
    ]


#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for pixo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from pixoapi.views import register_user, login_user, CollectibleView, PixoUserView, CategoryView, CartView, CartItemView, MessagesView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'collectibles', CollectibleView, 'collectible')
router.register(r'pixouser', PixoUserView, 'pixouser')
router.register(r'categories', CategoryView, 'categories')
router.register(r'cart', CartView, 'cart')
router.register(r'cartitems', CartItemView, 'cartitems')
router.register(r'messages', MessagesView, 'messages')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]

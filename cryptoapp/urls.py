"""
URL configuration for cryptoapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from userApp.views import SignUpView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('news/', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('music/', TemplateView.as_view(template_name='feature.html'), name='feature'),
    path('pages/', TemplateView.as_view(template_name='pages.html'), name='pages'),
    path('music/', TemplateView.as_view(template_name='roadmap.html'), name='roadmap'),
    path('music/', TemplateView.as_view(template_name='service.html'), name='service'),
    path('music/', TemplateView.as_view(template_name='token.html'), name='token'),
    path('music/', TemplateView.as_view(template_name='404.html'), name='404'),
    re_path(r'^accounts/', include ('django.contrib.auth.urls')),
    re_path(r'^accounts/signup/$', SignUpView.as_view(), name= "signup"),
    re_path(r'^userApp/', include('userApp.urls')),
    re_path(r'^paymentApp/', include('paymentApp.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
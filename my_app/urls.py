from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(60)(WomenHome.as_view()), name='home'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomanCategory.as_view(), name='category'),

    # For Base templates
    path('register/', RegisterUser.as_view(), name='register'),
    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]

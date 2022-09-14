from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView, AuthenticationForm, auth_login
from django.http import HttpResponseNotFound
from django.shortcuts import render, HttpResponse, get_object_or_404, Http404, redirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from main_project.settings import EMAIL_HOST_USER

from .utils import *
from .forms import *
from .models import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'my_app/women_info.html'
    context_object_name = 'womens'

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return context | c_def


# def show_category(request, cat_slug):
#     womens = Women.objects.filter(cat__slug=cat_slug)
#     cats = Category.objects.all()
#
#     if len(cats) == 0:
#         raise Http404()
#
#     context = {'womens': womens,
#                'cats': cats,
#                'menu_bar': menu_base,
#                'cat_selected': cat_slug
#                }
#     return render(request, 'my_app/women_info.html', context=context)

class WomanCategory(DataMixin, ListView):
    model = Women
    template_name = 'my_app/women_info.html'
    context_object_name = 'womens'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        title_title = 'Категория -' + str(c.name)
        c_def = self.get_user_context(title=title_title, cat_selected=c.slug)

        return context | c_def


# def home(request):
#     womens = Women.objects.all()
#     cats = Category.objects.all()
#     context = {'womens': womens,
#                'cats': cats,
#                'menu_bar': menu_base,
#                'cat_selected': 0
#                }
#     return render(request, 'my_app/women_info.html', context=context)


def about(request):
    user = request.user
    return HttpResponse(f'Hello {user}, this title on moderating')


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'my_app/post_details.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title_title = context['post'].title
        cat_selected = context['post'].cat.slug
        c_def = self.get_user_context(title=title_title, cat_selected=cat_selected)

        return context | c_def


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'my_app/add_page.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')

        return context | c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'my_app/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationUserForm
    template_name = "my_app/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'my_app/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        print(self.request)
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        print(form.cleaned_data['subject'], form.cleaned_data['content'])
        user = self.request.user
        messages.success(self.request, f'{user}, ваше успешно отправленно')
        text_massage = f'Обратная связь от пользователя\n' \
                       f'Текст обращения: {form.cleaned_data["content"]}'
        send_mail(form.cleaned_data['subject'], text_massage,
                  EMAIL_HOST_USER, ['tesslogun@gmail.com'], fail_silently=False)
        return redirect('contact')


# def add_page(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm
#
#     context = {
#         'form': form,
#         'menu_bar': menu_base,
#     }
#     return render(request, 'my_app/add_page.html', context=context)


# def contact(request):
#     return HttpResponse('U can write to us smf, its our contact: ')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

#
#
# def register(request):
#     return HttpResponse('register')

# def post_details(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'menu_bar': menu_base,
#         'cat_selected': post.cat.slug
#     }
#     return render(request, "my_app/post_details.html", context=context)

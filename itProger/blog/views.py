from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import News
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):
    data = {
        'news': News.objects.all(),
        'title': 'Главная страница блога'
    }
    return render(request, 'blog/home.html', data)


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 2 #по 2 записи на странице

    def get_context_data(self,  **kwargs):
        ctx = super(ShowNewsView, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница блога'
        return ctx


class NewsDetailView(DetailView):
    model = News
    def get_context_data(self,  **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)
        ctx['title'] = News.objects.filter(pk=self.kwargs['pk']).first() #filter для получения определенных записей по определенным критериям
        return ctx


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        else:
            return False


class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = '/' #перенаправляет на главную

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True
        else:
            return False


class UserAllNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 2 #по 2 записи на странице

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(avtor=user).order_by('-date')


    def get_context_data(self,  **kwargs):
        ctx = super(UserAllNewsView, self).get_context_data(**kwargs)
        ctx['title'] = f"Все статьи от пользователя {self.kwargs.get('username')}"
        return ctx


def contacti(request):
    return render(request, 'blog/contacti.html', {'title':'Страничка про нас'})

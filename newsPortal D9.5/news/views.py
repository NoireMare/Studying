from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from NewsPortal.settings import DEFAULT_FROM_EMAIL


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type=True).order_by('-time_add')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'


def news_filter(request):
    news = Post.objects.filter(type=True).order_by('-time_add')
    n_filter = PostFilter(request.GET, queryset=news)
    posts = n_filter.qs
    context = {
        'posts': posts,
        'n_filter': n_filter,
    }
    return render(request, 'news/search.html', context)


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    success_url = 'success'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = True
        return super().form_valid(form)


def send_emails_to_subscribers(request):
    post = Post.objects.all().last()
    title, text, id = [post.title, post.text, post.id]
    for cat in post.category_post.all():
        for subscriber in cat.category_user.all():
            html_content = render_to_string(
                'account/email/news_to_subscribers.html',
                {
                    'form': [title, text, id, subscriber.username],
                })
            msg = EmailMultiAlternatives(
                subject=f'{title}',
                body=f'{text}',
                from_email=DEFAULT_FROM_EMAIL,
                to=[subscriber.email],  # это то же, что и recipients_list
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html
            msg.send()  # отсылаем
    return redirect('/news')


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    permission_required = 'news.change_post'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('posts')
    permission_required = 'news.delete_post'


def posts_in_category(request, category_id):
    news = Post.objects.filter(type=True, category_post=category_id).order_by('-time_add')
    n_filter = PostFilter(request.GET, queryset=news)
    posts = n_filter.qs
    category = Category.objects.get(id=category_id)
    context = {
        'posts': posts,
        'n_filter': n_filter,
        'cat': category
    }
    return render(request, 'news_in_category.html', context)


class Categories(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'cats'












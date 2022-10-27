from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.filter(type=True).order_by('-time_add')
    paginate_by = 10


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

    #def get_queryset(self):
     #   queryset = super().get_queryset()
      #  self.filterset = PostFilter(self.request.GET, queryset)
       # return self.filterset.qs

    #def get_context_data(self, **kwargs):
     #   context = super().get_context_data(**kwargs)
      #  context['filterset'] = self.filterset
       # return context


class PostCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = True
        return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('posts')





from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Reply
from .forms import PostForm


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = 'created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'


class CategoryList(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_list'

    def get_queryset(self):
        queryset = Post.objects.filter(category=self.kwargs['category']).order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # category = [y for x, y in Post.CATEGORIES if x == self.kwargs['category']]
        # category = [item for item in Post.CATEGORIES if self.kwargs['category'] in item]
        category = dict(Post.CATEGORIES)
        # if category:
        #     context['category'] = category[0]
        #     context['category'] = category[0][1]
        if self.kwargs['category'] in category.keys():
            context['category'] = category[self.kwargs['category']]
        return context

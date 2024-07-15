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

    # def post(self, request, *args, **kwargs):
    #     form = PostForm(*args, **kwargs)
    #     # form = PostForm(*args, user=request.user, **kwargs)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = self.request.user.username
    #         post.save()
    #         return HttpResponseRedirect(reverse_lazy('board:post_details', args=[post.id]))
    #     return render(request, 'post_edit.html', {'form': form})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


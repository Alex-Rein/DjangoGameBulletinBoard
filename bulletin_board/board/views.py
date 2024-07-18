from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, Reply
from .forms import PostForm, ReplyForm


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

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj

    # def get_queryset(self, *args, **kwargs):
    #     return Post.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = 'post_list'
    template_name = 'post_delete'

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()
        return obj


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


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = Reply
    template_name = 'reply_edit.html'
    form_class = ReplyForm

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        post_ = Post.objects.get(pk=self.kwargs['pk'])
        reply.post = post_
        reply.save()
        post_.replies.add(reply)
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(ReplyCreate, self).get_context_data(**kwargs)
    #     context['object'] = self.object
    #     return context

    def dispatch(self, request, *args, **kwargs):  # Проверка что на свое сообщение нельзя оставлять отклик
        author = Post.objects.get(pk=self.kwargs['pk']).author
        if request.user == author:
            return HttpResponseRedirect(reverse('post_details', args=[self.kwargs['pk']]))
        return super().dispatch(request, *args, **kwargs)


class BoardPostsList(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-created'
    template_name = 'board_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method == "GET":
            return queryset.filter(author=self.request.user)
        return Post.objects.none()

    def dispatch(self, request, *args, **kwargs):  # Проверка чтобы можно было войти только в свою борду
        # print('==============')
        # print(request.user, self.kwargs['username'], request.user.username == self.kwargs['username'])
        # print('==============')
        if request.user.username != self.kwargs['username']:
            # print('if')
            return HttpResponseRedirect(reverse_lazy('board', args=[request.user.username]))
        # print('else')
        return super().dispatch(request, *args, **kwargs)


class BoardPostReplies(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'board_post_replies.html'
    context_object_name = 'replies'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BoardPostReplies, self).get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['title'] = post.title
        context['category'] = post.get_category_display
        context['created'] = post.created
        print('===============')
        print(context)
        print('===============')
        return context

    def get_queryset(self):
        post_ = get_object_or_404(Post, id=self.kwargs['pk'])
        queryset = post_.replies.all().order_by('-created')
        return queryset

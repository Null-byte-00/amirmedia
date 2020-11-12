from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import Postform, Commentform
from .models import Post, Comment
from mainapp.models import Profile
from taggit.models import Tag
# Create your views here.


class Postslist(ListView):
    """
    shows 20 newest posts
    """
    queryset = Post.objects.order_by('-date_published')[:20]
    template_name = 'userpost/posts.html'
    context_object_name = 'posts'


class UserPosts(ListView):
    """
    shows posts from one specific user
    """
    queryset = Post.objects.all()
    template_name = 'userpost/user_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        username = self.kwargs['username']
        profile = get_object_or_404(Profile, slug=username)
        user = profile.user
        posts = Post.objects.filter(user=user)
        return posts

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user'] = self.kwargs['username']
        return context


class Showpost(DetailView):
    """
    renders a post
    """
    queryset = Post.objects.all()
    template_name = 'userpost/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, pk=self.kwargs['id'])
        comments = Comment.objects.filter(post=post)
        context['comments'] = comments
        return context

    def get_object(self, queryset=None):
        profile = get_object_or_404(Profile, slug=self.kwargs['username'])
        user = profile.user
        post = get_object_or_404(Post, user=user, slug=self.kwargs['post'], id=self.kwargs['id'])
        return post


class Addpost(LoginRequiredMixin, FormView):
    """
    creates a Post object from given information
    and redirects the user to signin page if user is not logged in
    """
    form_class = Postform
    template_name = 'userpost/add_post.html'
    login_url = '/signin/'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        form.save_m2m()
        # self.success_url = '/posts/' + self.request.user.profile.slug + '/' + post.slug
        self.success_url = reverse('userpost:post',
        kwargs={'username': self.request.user.profile.slug,
        'id': post.pk,
        'post': post.slug})

        return super().form_valid(form)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['common_tags'] = Post.tags.most_common()[:7]
        return context


class TaggedPost(ListView):
    """
    filters posts with one tag
    """
    queryset = Post.objects.all()
    template_name = 'userpost/tagged_post.html'
    context_object_name = 'posts'

    def get_queryset(self, **kwargs):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        posts = Post.objects.filter(tags=tag)
        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['t'] = self.kwargs['tag']
        return context


# adds a comment from current user to the Post with given pk
def add_comment(request):
    if not request.user.is_authenticated:
        return redirect('/signin/')
    form = Commentform(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        post = get_object_or_404(Post, id=form.cleaned_data.get('post_id'))
        user = request.user
        comment.post = post
        comment.user = user
        comment.save()
        return redirect(reverse('userpost:post', kwargs={ 'username': post.user.profile.slug,'id': post.pk, 'post': post.slug}))
    else:
        return HttpResponse('something went wrong')




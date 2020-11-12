from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, UpdateView
from django.contrib.auth.models import User
from mainapp.models import Profile
from userpost.models import Post
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.


class ProfileDetail(DetailView):
    """
    shows profile information
    """
    queryset = User.objects.all()
    template_name = 'userprofile/profile_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if self.request.user.profile.slug == self.kwargs['username']:
                context['is_this_user'] = True
        profile = Profile.objects.get(slug=self.kwargs['username'])
        posts = Post.objects.filter(user=profile.user).order_by('-date_published')
        context['latest_posts'] = posts[:3]
        return context

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        profile = get_object_or_404(Profile, slug=username)
        return profile


class Profileedit(UpdateView):
    """
    updates profile fields
    """
    queryset = Profile.objects.all()
    template_name = 'userprofile/profile_edit.html'
    fields = ['gender', 'age', 'location', 'bio', 'profilepic']
    success_url = '../'

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        profile = get_object_or_404(Profile, slug=username)
        return profile

    def get(self, request, *args, **kwargs):
        # check if this profile is for current user
        if self.request.user.is_authenticated:
            if self.request.user.profile.slug == self.kwargs['username']:
                return super().get(request, *args, **kwargs)
        return redirect('/signin/')

    def post(self, request, *args, **kwargs):
        # check also if http method is post to prevent http verb tampering
        if self.request.user.is_authenticated:
            if self.request.user.profile.slug == self.kwargs['username']:
                return super().post(request, *args, **kwargs)
        return redirect('/signin/')


# redirects the current user to its profile
def redirect_profile(request):
    if not request.user.is_authenticated:
        return redirect('/signin/')
    user = request.user
    return redirect(reverse('userprofile:profile', kwargs={'username': user.profile.slug}))
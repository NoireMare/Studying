from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def change_group_to_authors(request):
    authors_group = Group.objects.get(name='authors')
    user = request.user
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/accounts/profile/')


@login_required
def change_group_to_common(request):
    authors_group = Group.objects.get(name='authors')
    user = request.user
    if user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
    return redirect('/accounts/profile/')



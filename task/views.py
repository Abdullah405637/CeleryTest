from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect

from .form import GenerateRandomUserForm
from .tasks import create_random_user_accounts

# returns a list of generated user accounts
class UsersListView(ListView):
    template_name = 'task/user_list.html'
    model = User

# A page with the form where we can input the number of accounts to generate
class GenerateRandomUserView(FormView):
    template_name = 'task/generate_random_user.html'
    form_class = GenerateRandomUserForm

    def form_valid(self, form):
        total = form.cleaned_data.get('total')
        create_random_user_accounts.delay(total)
        messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')
        return redirect('users_list')
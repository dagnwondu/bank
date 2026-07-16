from . models import CustomUser
from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.utils.timezone import now
from django.contrib.auth import update_session_auth_hash, logout, get_user_model, authenticate, login, get_user_model
from django.contrib.auth.views import LoginView
from . forms import UserForm
from .forms import UserUpdateForm  
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(settings.LOGIN_URL) # Use the setting, not a hardcoded string
            if request.user.user_type not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Cashier views
# Cashier views
# Cashier views
@role_required(['cashier'])
def cashier_dashboard(request):
   
    return render(request, 'dashboards/cashier_dashboard.html')

# finance views
# finance views
# finance views
@role_required(['finance'])
def finance_dashboard(request):
 

    return render(request, 'dashboards/finance_dashboard.html')

# Admin views
# Adminviews
# Adminviews
@role_required(['admin'])
def admin_dashboard(request):
    # -------------------------
    # HANDLE POST (Create User)
    # -------------------------
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error while creating User")
    else:
        user_form = UserForm()

    # -------------------------
    # SORTING PARAMETERS
    # -------------------------
    sort_by = request.GET.get('sort', 'id')
    direction = request.GET.get('direction', 'asc')

    sort_order = f"-{sort_by}" if direction == "desc" else sort_by

    # -------------------------
    # FETCH USERS (Exclude superuser)
    # -------------------------
    users_list = CustomUser.objects.exclude(is_superuser=True).order_by(sort_order)

    # -------------------------
    # PAGINATION
    # -------------------------
    paginator = Paginator(users_list, 5)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    # -------------------------
    # CONTEXT
    # -------------------------
    context = {
        'users': users,
        'sort_by': sort_by,
        'direction': direction,
        'user_form': user_form,
    }

    return render(request, 'dashboards/admin_dashboard.html', context)

# def dashboard(request):
#     role_map = {
#         'customer': 'customer_dashboard',
#         'finance': 'finance_dashboard',
#         'admin': 'admin_dashboard',
#         'accountant': 'accountant_dashboard',
#         'cashier': 'cashier_dashboard',
#     }
    
#     # Get the role and redirect safely
#     target_view = role_map.get(request.user.user_type.lower())
    
#     if target_view:
#         return redirect(target_view)
        
#     messages.error(request, 'Unauthorized access.')
#     return redirect('login') # Assuming you have a 'login' URL name

class MyUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name = 'users/users_management.html'
    context_object_name = 'users'
    paginate_by = 10

    # 🔐 Role restriction
    def test_func(self):
        return self.request.user.user_type == 'admin'

    def handle_no_permission(self):
        messages.error(self.request, "You are not allowed to access this page.")
        return redirect('dashboard')  # change if needed

    # 📦 Extra context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault('user_form', UserForm())
        return context

    # ➕ Handle user creation
    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            messages.success(request, "User created successfully!")
            return redirect('users_management')

        # ❌ Form invalid
        messages.error(request, "Error while creating user.")

        self.object_list = self.get_queryset()
        context = self.get_context_data(user_form=user_form)
        return render(request, self.template_name, context)
class MyStaffsView(LoginRequiredMixin, ListView):
    template_name = 'admin_page/manage_staffs.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()  # Initialize object_list
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('staffs_management')
        messages.error(request, "Error while creating Staff")
        self.object_list = self.get_queryset()  # Ensure object_list is set
        context = self.get_context_data()
        context['user_form'] = user_form  # Include form with errors
        return render(request, self.template_name, context)
@login_required
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)

        if form.is_valid():
            
            form.save()
            messages.success(request, f"'User {user} Updated Successfully'")

            return redirect("admin_dashboard")
    else:
        form = UserUpdateForm(instance=user)

    return render(request, "partials/update_user.html", {"form": form})
@login_required
def delete_user(request, user_id):
    # Only allow deletion if the user exists
    user = get_object_or_404(CustomUser, id=user_id)
    
    # Prevent deletion of yourself
    if request.user == user:
        messages.error(request, "You cannot delete yourself.")
        return redirect(reverse('users_management'))  # Update 'manage_users' with your actual view name

    # Delete the user
    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect(reverse('users_management'))  # Update 'manage_users' with your actual view name
@login_required
def change_password(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
        else:
            messages.error(request, "Passwords do not match.")

    return redirect('users_management')  # Adjust to your URL name

# Staffs Management
@login_required
def update_staff(request, staff_id):

    return render(request, "admin_page/update_staff.html")


@login_required
def change_password(request, user_id):
    user = CustomUser.objects.get(id=user_id)

    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully!")
        else:
            messages.error(request, "Passwords do not match.")

    return redirect('users_management')  # Adjust to your URL name

# def doctor_page(request):
#     user = request.user
#     return render(request, 'dashboard/dashboard.html')


@login_required
def logout(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
        logout(request)
        return redirect('/')  
def password_change(request):  
    return redirect('/accounts/password_change/')
# Error Pages
def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)
def custom_403(request, exception):
    return render(request, 'errors/403.html', status=403)
def custom_500(request):
    return render(request, 'errors/500.html', status=500)







def login_page(request):
    return render(request, 'registration/login.html')
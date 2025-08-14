from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm,RegisterForm,AssignRoleForm,CreateGroupForm
from .models import Event
from .forms import EventForm
from .models import Participant
from .forms import ParticipantForm
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth import login , logout, authenticate
from django.db.models import Q

from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.urls import reverse
import datetime
from django.shortcuts import render
from .models import Event, Participant
from django.contrib.auth.models import User,Group
from django.db import models
from django.contrib.auth.decorators import login_required , user_passes_test,permission_required
from events.signals import send_activation_email
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render,  redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .forms import ProfileForm,UserForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView,DeleteView,CreateView , ListView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView

def is_admin(user) :
    return user.groups.filter(name ='Admin').exists()


def is_manager(user) :
    return user.groups.filter(name ='Manager').exists()


def is_organizer(user) :
    return user.groups.filter(name ='Organizer').exists()

# def category_list(request):
#     category = Category.objects.all()
#     return render(request, 'category_list.html', {'categories': category})

class CategoryList(LoginRequiredMixin,ListView):

    model = Category

    template_name = 'category_list.html'


    context_object_name = 'categories'



# @login_required
# @permission_required("events.add_category", login_url='no-permission')
# def category_create(request):

#     form = CategoryForm()

#     if request.method == 'POST':


#         form = CategoryForm(request.POST)

#         if form.is_valid():
#             form.save()

#             return redirect('category-list')

#     return render(request,'category_form.html',{'form': form})

class CategoryCreate(LoginRequiredMixin , PermissionRequiredMixin,CreateView):

    model = Category

    form_class = CategoryForm


    template_name = 'category_form.html'

    permission_required = 'events.add_category'
    success_url = reverse_lazy('category-list')




# @login_required
# @permission_required("events.change_category", login_url='no-permission')
# def category_update(request, id):
#     category = Category.objects.get(id = id)
#     # form = CategoryForm()
#     if request.method == 'POST':

#         form = CategoryForm(request.POST, instance=category)

#         if form.is_valid():
#             form.save()
#             return redirect('category-list')
        
#     else:
#         form = CategoryForm(instance=category)
        
#     return render(request,'category_form.html', {'form': form})


class CategoryUpdate(LoginRequiredMixin , PermissionRequiredMixin , UpdateView):
    model = Category

    form_class = CategoryForm

    template_name = 'category_form.html'

    permission_required = 'events.change_category'

    success_url = reverse_lazy('category-list')


# @login_required
# @permission_required("events.delete_category", login_url='no-permission')
# def category_delete(request, id):
#     category = Category.objects.get(id = id)
#     if request.method == 'POST':

#         category.delete()
#         return redirect('category-list')
    

#     return render(request,'category_confirm_delete.html', {'category': category})





class CategoryDelete(LoginRequiredMixin, PermissionRequiredMixin,   DeleteView) :
    
    model = Category

    template_name = 'category_confirm_delete.html'

    permission_required = "events.delete_category"

    success_url = reverse_lazy('category-list')



def home(request) :
    return render(request,'home.html')

# @login_required
# @permission_required("events.add_event", login_url='no-permission')
# def event_create(request):

#     form = EventForm()

#     if request.method == 'POST':

#         form = EventForm(request.POST,request.FILES)

#         if form.is_valid():
#             form.save()
#             if request.user.groups.filter(name='Admin').exists():
#                 return redirect('admin-dashboard')
#             elif request.user.groups.filter(name='Organizer').exists():
#                 return redirect('organizer-dashboard')

#     return render(request,'event_form.html', {'form': form})



class EventCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView) :

    model = Event
    form_class = EventForm

    template_name = 'event_form.html'
    permission_required = 'events.add_event'


    def get_success_url(self):
        if self.request.user.groups.filter(name = 'Admin').exists() :

            return reverse_lazy('admin-dashboard')
        
        elif self.request.user.groups.filter(name = 'Organizer').exists() :
            return reverse_lazy('organizer-dashboard')


@login_required
@permission_required("events.change_event", login_url='no-permission')
def event_update(request,id):
    event =Event.objects.get(id = id)

    # form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)

        if form.is_valid():
            form.save()

            if request.user.groups.filter(name='Admin').exists():
                return redirect('admin-dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer-dashboard')
            
    else:
        form = EventForm(instance=event)

    return render(request,'event_form.html',{'form': form})




@login_required
@permission_required("events.delete_event", login_url='no-permission')
def event_delete(request, id):
    event = Event.objects.get(id = id)

    if request.method == 'POST': 

        event.delete()

        if request.user.groups.filter(name='Admin').exists():

            return redirect('admin-dashboard')
        elif request.user.groups.filter(name='Organizer').exists():
            return redirect('organizer-dashboard')
        
    return render(request,'event_confirm_delete.html',{'event': event})




 
def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    event = Event.objects.first()

    return render(request, 'participant_list.html',{'participants': participants, 'event': event})




@login_required
@permission_required("events.add_participant", login_url='no-permission')
def participant_create(request, event_id):

    event = Event.objects.get(id = event_id)
    form = ParticipantForm()

    if request.method == 'POST':

        form = ParticipantForm(request.POST, event_instance=event)

        if form.is_valid():
            participant = form.save()

            return redirect('event_list')

    return render(request,'participant_form.html',{'form': form,'event': event})




@login_required
@permission_required("events.delete_participant", login_url='no-permission')
def participant_delete(request, id):
    participant = Participant.objects.get(id = id)

    if request.method == 'POST':
        participant.delete()

        if request.user.groups.filter(name='Admin').exists():
            return redirect('admin-dashboard')

        

    return render(request,'participant_confirm_delete.html', {'participant': participant})








def register_page(request) :


    form = RegisterForm()

    if request.method =='POST' :
        form = RegisterForm(request.POST)

        if form.is_valid() :

            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password1'))
            user.is_active = False 

            user.save()
            messages.success(request, 'Please check your email to activate your account.')
            return redirect('sign-in')
        
    return render(request,'register_form.html',{'form' : form})



def active_account(request, user_id, token):
    user = User.objects.get(id=user_id)



    if default_token_generator.check_token(user, token):
        user.is_active = True


        user.save()
        messages.success(request, "Your account has been activated successfully! You can now log in.")

        return redirect('sign-in')
    else:
        messages.error(request, "Activation link is invalid or has expired.")
        return redirect('sign-up')



def login_page(request) :
    

    form = AuthenticationForm()
    if request.method == 'POST' :

        username = request.POST.get('username') 
        password =  request.POST.get('password')

        user = authenticate(username=username,password=password)


        if user is not None :
            if user.is_active:

                login(request, user)
                return redirect('home')
            else:

                messages.error(request, "Your account is not active. Please activate it first.")

        else:
            messages.error(request, "Invalid username or password.")
            

    return render(request, 'login_page.html', {"form" : form})  












def event_list(request):
    search_query = request.GET.get('search', '')
    category_id = request.GET.get('category')



    events = Event.objects.select_related('category').all()

    if search_query:
        events = events.filter(
            models.Q(title=search_query) |
            models.Q(location=search_query)
        )

    if category_id:
        events = events.filter(category_id=category_id)


    categories = Category.objects.all()

    context = {
        'events': events,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'event_list.html', context)




def event_detail(request, id):

    event = Event.objects.get(id = id)
    participants = Participant.objects.filter(events=event)


    search = request.GET.get('search', '')

    if search:
        participants = Participant.objects.filter(
            events=event
        ).filter(
            models.Q(name=search) | models.Q(email=search)
        )

        

    context = {
        'event': event,
        'participants': participants,
        'search_query': search,
    }

    return render(request,'event_details.html', context)





@login_required
@user_passes_test(is_organizer, login_url='no-permission')
def organizer_dashboard(request):

    total_events = Event.objects.count()

    total_participants = Participant.objects.count()


    events = Event.objects.order_by('-date')

    context = {
        'total_events': total_events,
        'total_participants': total_participants,

        'recent_events': events,
    }
    return render(request, 'dashboard/organizer.html', context)



@login_required
@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    event_search = request.GET.get('event_search', '')

    participant_search = request.GET.get('participant_search', '')

    user_search = request.GET.get('user_search', '')



    events = Event.objects.all()

    if event_search:
        events = events.filter(
            Q(title=event_search) 

        )


    participants = Participant.objects.all()

    if participant_search:

        participants = participants.filter(
            Q(name=participant_search) |
            Q(email=participant_search)
        )


    users = User.objects.all()

    if user_search:

        users = users.filter(
            Q(username=user_search) |
            Q(email=user_search)
        )

    context = {
        'events': events,
        'participants': participants,
        'users': users,
        'event_search': event_search,
        'participant_search': participant_search,
        'user_search': user_search,
    }
    return render(request, 'dashboard/admin.html', context)





@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request,user_id) :

    user = User.objects.get(id =user_id)

    form = AssignRoleForm()

    if request.method == 'POST' :

        form = AssignRoleForm(request.POST)

        if form.is_valid() :

            role = form.cleaned_data['role']

            user.groups.clear()
            user.groups.add(role)
            return redirect('admin-dashboard')
    

    return render(request,'dashboard/assign_role.html',{ "form" :form})



@user_passes_test(is_admin, login_url='no-permission')
def create_group(request) :
    form = CreateGroupForm()


    if request.method == 'POST' :
        form = CreateGroupForm(request.POST)


        if form.is_valid():
            group =form.save()
            return redirect('admin-dashboard')
        
    return render(request,'dashboard/create_group.html', {"form" : form})

@user_passes_test(is_admin, login_url='no-permission')
def group_list(request) :
    groups = Group.objects.all()

    return render(request,'dashboard/group_list.html', {"groups" : groups})


@login_required
def logout_page(request):

    if request.method == 'POST':
        logout(request)
        return redirect('home')
    

def no_permission(request) :

    return render(request,'dashboard/page_not_found.html')



@login_required
@permission_required('auth.change_group', raise_exception=True)
def group_update(request, group_id):
    group = Group.objects.get(id = group_id)
    all_permissions = Permission.objects.all()



    if request.method == 'POST':

        name = request.POST.get('name')
        permission = request.POST.getlist('permissions')

        if name:

            group.name = name
            group.save()


            permissions = Permission.objects.filter(id__in=permission)
            group.permissions.set(permissions)

            return redirect('group-list')


    group_permissions = group.permissions.all().values_list('id', flat=True)

    context = {
        'group': group,
        'all_permissions': all_permissions,
        'group_permissions': group_permissions,
    }

    return render(request, 'dashboard/group_update.html', context)



def group_delete(request, group_id):
    group = Group.objects.get(id =group_id)

    if request.method == 'POST':

        group.delete()
        return redirect('group-list')

    return render(request,'dashboard/group_confirm_delete.html', {'group': group})



@login_required
def profile_view(request):
    profile = request.user.profile
    user = request.user


    return render(request, 'profile.html', {'profile': profile , 'user': user})




@login_required
def edit_profile(request):

    user = request.user
    profile = user.profile


    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)

        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)


        if user_form.is_valid() and profile_form.is_valid():
            
            user_form.save()
            profile_form.save()


            return redirect('profile')
    else:

        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    context = {'profile_form': profile_form}
    return render(request, 'edit_profile.html', context)




def change_password(request):


    if request.method == "POST":

        current_password = request.POST.get("current_password")

        new_password = request.POST.get("new_password")


        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):

            messages.error(request, "Current password is incorrect.")


            return redirect("change-password")

        if new_password != confirm_password:
            messages.error(request, "password  do not match.")
            return redirect("change-password")

        request.user.set_password(new_password)


        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Password changed successfully.")


        return redirect("profile")

    return render(request, "change_password.html")


def reset_password_request(request):


    if request.method == 'POST':
        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()


        if not user:
            messages.error(request, "No user found with this email.")


            return redirect('reset-password')

        token = get_random_string(length=50)


        if hasattr(user, 'profile'):


            user.profile.reset_token = token

            user.profile.save()
        else:

            messages.error(request, "User profile not found.")
            return redirect('reset-password')

        reset_link = request.build_absolute_uri(

            reverse('reset-confirm', args=[user.id, token])


        )

        send_mail(
            subject="Password Reset",
            message=f"Click here to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            
            recipient_list=[email],
        )

        messages.success(request, "Password reset link sent to your email.")
        return redirect('sign-in')

    return render(request, 'reset_password.html')





def reset_password_confirm(request, user_id, token):
    user = User.objects.filter(id=user_id, profile__reset_token=token).first()


    if not user:

        messages.error(request, "Invalid or expired reset link.")


        return redirect('reset-password')

    if request.method == 'POST':


        new_password = request.POST.get('new_password')


        confirm_pass = request.POST.get('confirm_password')


        if new_password != confirm_pass:

            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        user.set_password(new_password)


        user.save()

        user.profile.reset_token = ''


        user.profile.save()
        messages.success(request, "Password reset successful! You can now log in.")
        return redirect('sign-in')


    return render(request, 'reset_confirm.html')
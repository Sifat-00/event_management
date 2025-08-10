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


def is_admin(user) :
    return user.groups.filter(name ='Admin').exists()


def is_manager(user) :
    return user.groups.filter(name ='Manager').exists()


def is_organizer(user) :
    return user.groups.filter(name ='Organizer').exists()

def category_list(request):
    category = Category.objects.all()
    return render(request, 'category_list.html', {'categories': category})


@login_required
@permission_required("events.add_category", login_url='no-permission')
def category_create(request):

    form = CategoryForm()

    if request.method == 'POST':


        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('category-list')

    return render(request,'category_form.html',{'form': form})


@login_required
@permission_required("events.change_category", login_url='no-permission')
def category_update(request, id):
    category = Category.objects.get(id = id)
    # form = CategoryForm()
    if request.method == 'POST':

        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect('category-list')
        
    else:
        form = CategoryForm(instance=category)
        
    return render(request,'category_form.html', {'form': form})

@login_required
@permission_required("events.delete_category", login_url='no-permission')
def category_delete(request, id):
    category = Category.objects.get(id = id)
    if request.method == 'POST':

        category.delete()
        return redirect('category-list')
    

    return render(request,'category_confirm_delete.html', {'category': category})

def home(request) :
    return render(request,'home.html')



@login_required
@permission_required("events.add_event", login_url='no-permission')
def event_create(request):

    form = EventForm()

    if request.method == 'POST':

        form = EventForm(request.POST,request.FILES)

        if form.is_valid():
            form.save()
            if request.user.groups.filter(name='Admin').exists():
                return redirect('admin-dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer-dashboard')

    return render(request,'event_form.html', {'form': form})



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
            # send_activation_email(request, user)
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

    #    if form.is_valid() :
    #         form = AuthenticationForm(data = request.POST)
    #         user = form.get_user()
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



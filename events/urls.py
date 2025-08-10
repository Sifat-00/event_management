from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('categories/', views.category_list, name='category-list'),
    path('categories-create/', views.category_create, name='category-create'),
    path('categories-update/<int:id>/', views.category_update, name='category-update'),
    path('categories-delete/<int:id>/', views.category_delete, name='category-delete'),

 
    path('events/', views.event_list, name='event_list'),
    path('events-create/', views.event_create, name='event-create'),
    path('events-update/<int:id>/', views.event_update, name='event_update'),
    path('events-delete/<int:id>/', views.event_delete, name='event_delete'),
    path('events-detail/<int:id>/', views.event_detail, name='event-detail'),





    path('participants/', views.participant_list, name='participant_list'),
    path('participants-create/<int:event_id>/', views.participant_create, name='participant_create'),
    path('participants-delete/<int:id>/', views.participant_delete, name='participant_delete'),





    path('home/',views.home, name='home'),

    path('sign-in',views.login_page, name='sign-in'),
    path('sign-up',views.register_page, name='sign-up'),

    path('organizer-dashboard/',views.organizer_dashboard,name='organizer-dashboard'),
    path('admin-dashboard/',views.admin_dashboard,name='admin-dashboard'),
    path('assign-role/<int:user_id>',views.assign_role, name='assign-role'),
    path('create-role/',views.create_group, name='create-group'),
    path('group_list/',views.group_list, name='group-list'),
    path('logout/',views.logout_page, name='logout'),
    path('no-permission',views.no_permission, name='no-permission'),


    path('groups-update/<int:group_id>/', views.group_update, name='group-update'),
    path('groups-delete/<int:group_id>/', views.group_delete, name='group-delete'),


      path('activate/<int:user_id>/<str:token>/', views.active_account, name='activate-account'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
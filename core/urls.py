from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    path('', views.home, name='index'),  # Alias to satisfy templates using 'index'

    # Destinations list + alias used by templates
    path('destinations/', views.destination_list, name='destination_list'),
    path('destination/', views.destination_list, name='destination'),

    # Destination detail
    path('destinations/<slug:slug>/', views.destination_detail, name='destination_detail'),

    # Search and categorization
    path('search/', views.search_destinations, name='search_destinations'),
    path('category/<slug:category_slug>/', views.destinations_by_category, name='destinations_by_category'),
    path('type/<str:destination_type>/', views.destinations_by_type, name='destinations_by_type'),

    # Static-like pages backed by templates
    path('about/', views.about, name='about'),
    path('hotel/', views.hotel, name='hotel'),
    path('courses/', views.courses, name='courses'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('caravans/', views.caravan_list, name='caravan_list'),
    path('caravans/<slug:slug>/', views.caravan_detail, name='caravan_detail'),
    path('contact/', views.contact, name='contact'),
]
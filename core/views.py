from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Destination, Testimonial, Category, Course, Exam, CourseApplication
from .forms import SearchForm, CourseApplicationForm, AgencyRegistrationForm
from agency.models import Agency

def destination_list(request):
    # Get all destinations
    destinations_list = Destination.objects.filter(is_active=True).order_by('name')
    
    # Initialize search form
    form = SearchForm(request.GET or None)
    search_query = {}
    
    # Apply filters if form is submitted
    if form.is_valid():
        destination_name = form.cleaned_data.get('destination')
        price_limit = form.cleaned_data.get('price_limit')
        
        if destination_name:
            destinations_list = destinations_list.filter(
                Q(name__icontains=destination_name) | 
                Q(location__icontains=destination_name)
            )
            search_query['destination'] = destination_name
            
        if price_limit:
            destinations_list = destinations_list.filter(price_per_person__lte=price_limit)
            search_query['price_limit'] = price_limit
            
        # Store other search parameters
        search_query['checkin'] = request.GET.get('checkin', '')
        search_query['checkout'] = request.GET.get('checkout', '')
    
    # Pagination
    paginator = Paginator(destinations_list, 9)  # Show 9 destinations per page
    page = request.GET.get('page')
    
    try:
        destinations = paginator.page(page)
    except PageNotAnInteger:
        destinations = paginator.page(1)
    except EmptyPage:
        destinations = paginator.page(paginator.num_pages)
    
    # Get featured destinations
    featured_destinations = Destination.objects.filter(
        is_active=True, 
        is_featured=True
    )[:3]
    
    context = {
        'destinations': destinations,
        'featured_destinations': featured_destinations,
        'search_query': search_query,
        'page_title': 'Explore Destinations',
        'form': form,
    }
    
    return render(request, 'core/destination.html', context)

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug, is_active=True)
    
    # Get gallery images
    gallery_images = destination.images.all()
    
    # Get related destinations (same type)
    related_destinations = Destination.objects.filter(
        is_active=True,
        destination_type=destination.destination_type
    ).exclude(id=destination.id)[:3]
    
    # Get testimonials for this destination
    testimonials = destination.testimonials.filter(is_active=True)[:5]
    # Points of interest for mini-map
    pois = destination.points_of_interest.all()
    
    context = {
        'destination': destination,
        'gallery_images': gallery_images,
        'related_destinations': related_destinations,
        'testimonials': testimonials,
        'page_title': f'{destination.name} - West Bengal Tourism',
        'pois': pois,
    }
    
    return render(request, 'core/destination_detail.html', context)

def home(request):
    featured_destinations = Destination.objects.filter(
        is_active=True,
        is_featured=True
    )[:6]

    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:5]

    categories = Category.objects.all()

    all_destinations = Destination.objects.filter(is_active=True).only('name')

    # Build destination types with counts: (code, display, count)
    type_map = dict(Destination.DESTINATION_TYPES)
    destination_types = []
    for code, display in Destination.DESTINATION_TYPES:
        count = Destination.objects.filter(is_active=True, destination_type=code).count()
        destination_types.append((code, display, count))

    # Popular cities from existing destinations
    popular_cities = list(
        Destination.objects.filter(is_active=True)
        .values_list('location', flat=True)
        .distinct()[:10]
    )

    # Stats
    stats = {
        'destinations_count': Destination.objects.filter(is_active=True).count(),
        'tours_count': Destination.objects.filter(is_active=True).count(),
        'visitors_count': 10000,
    }

    # Placeholder discounted queryset (reuse featured)
    discounted_destinations = Destination.objects.filter(is_active=True, is_featured=True)

    services = [
        {
            'image': 'images/services-1.jpg',
            'icon': 'flaticon-paragliding',
            'title': 'Activities',
            'description': 'Curated local activities and experiences',
        },
        {
            'image': 'images/services-2.jpg',
            'icon': 'flaticon-route',
            'title': 'Travel Arrangements',
            'description': 'End-to-end planning and bookings',
        },
        {
            'image': 'images/services-3.jpg',
            'icon': 'flaticon-tour-guide',
            'title': 'Private Guide',
            'description': 'Knowledgeable local guides',
        },
        {
            'image': 'images/services-4.jpg',
            'icon': 'flaticon-map',
            'title': 'Location Manager',
            'description': 'On-ground support for your trip',
        },
    ]

    context = {
        'featured_destinations': featured_destinations,
        'testimonials': testimonials,
        'categories': categories,
        'all_destinations': all_destinations,
        'popular_cities': popular_cities,
        'destination_types': destination_types,
        'stats': stats,
        'discounted_destinations': discounted_destinations,
        'services': services,
        'show_video_section': False,
        'blog_posts': [],
        'page_title': 'West Bengal Tourism - Discover Beautiful Destinations',
    }
    
    return render(request, 'core/index.html', context)


def about(request):
    # Get existing testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    # Demo data for non-authenticated users
    demo_testimonials = [
        {
            'name': 'Priya Sharma',
            'position': 'Travel Enthusiast',
            'feedback': 'Amazing experience exploring the Sundarbans! The tour guides were knowledgeable and the accommodations were perfect. Will definitely recommend to friends and family.',
            'rating': 5,
            'image': None
        },
        {
            'name': 'Rajesh Kumar',
            'position': 'Photography Lover',
            'feedback': 'Darjeeling was absolutely breathtaking. The tea gardens, the mountain views, and the local culture made this trip unforgettable. Pacific Tourism made everything seamless.',
            'rating': 5,
            'image': None
        },
        {
            'name': 'Anita Das',
            'position': 'Cultural Explorer',
            'feedback': 'The heritage walk in Kolkata was incredible! Learned so much about the city\'s rich history and colonial architecture. Our guide was passionate and informative.',
            'rating': 4,
            'image': None
        },
        {
            'name': 'Suresh Patel',
            'position': 'Adventure Seeker',
            'feedback': 'Kalimpong was a hidden gem! The trekking routes were challenging but rewarding, and the local homestay experience was authentic. Pacific Tourism exceeded expectations.',
            'rating': 5,
            'image': None
        }
    ]
    
    # Handle testimonial submission for authenticated users
    form = None
    form_success = False
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            from .forms import TestimonialForm
            form = TestimonialForm(request.POST)
            if form.is_valid():
                testimonial = form.save(commit=False)
                testimonial.name = request.user.get_full_name() or request.user.username
                testimonial.position = 'Verified Tourist'
                testimonial.is_active = True
                testimonial.save()
                form_success = True
                form = TestimonialForm()
                # Refresh testimonials to include the new one
                testimonials = Testimonial.objects.filter(is_active=True).order_by('-created_at')[:8]
        else:
            from .forms import TestimonialForm
            form = TestimonialForm()
    
    # Combine demo data with real testimonials
    all_testimonials = list(testimonials) + demo_testimonials
    
    context = {
        'page_title': 'About Us',
        'testimonials': all_testimonials,
        'form': form,
        'form_success': form_success,
        'user_authenticated': request.user.is_authenticated,
    }
    return render(request, 'core/about.html', context)


def hotel(request):
    from .models import Caravan
    agencies = Agency.objects.filter(approved=True).order_by('name')
    reg_form = AgencyRegistrationForm(request.POST or None, request.FILES or None)
    reg_success = False
    if request.method == 'POST' and reg_form.is_valid():
        reg_form.save()
        reg_success = True
        reg_form = AgencyRegistrationForm()

    # Get featured caravans for the travel agency section
    featured_caravans = Caravan.objects.filter(is_active=True, is_available=True, is_featured=True)[:6]
    
    # Get caravan types for filtering
    caravan_types = Caravan.CARAVAN_TYPES

    context = {
        'page_title': 'Travel Agency',
        'agencies': agencies,
        'agency_form': reg_form,
        'agency_reg_success': reg_success,
        'featured_caravans': featured_caravans,
        'caravan_types': caravan_types,
    }
    return render(request, 'agency/hotel_base.html', context)


def courses(request):
    courses_list = Course.objects.filter(is_active=True).order_by('name')
    
    # Get category filter from query params
    category_filter = request.GET.get('category', '')
    if category_filter:
        courses_list = courses_list.filter(category=category_filter)
    
    # Get featured courses
    featured_courses = Course.objects.filter(is_active=True, is_featured=True)[:3]
    
    # Get all categories for filter
    categories = Course.COURSE_CATEGORIES
    
    # Pagination
    paginator = Paginator(courses_list, 9)
    page = request.GET.get('page')
    
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)

    context = {
        'page_title': 'Courses',
        'courses': courses,
        'featured_courses': featured_courses,
        'categories': categories,
        'current_category': category_filter,
    }
    return render(request, 'core/courses.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    # Get related courses (same category)
    related_courses = Course.objects.filter(
        is_active=True,
        category=course.category
    ).exclude(id=course.id)[:3]
    
    # Get course application form
    form = CourseApplicationForm(request.POST or None)
    form_success = False
    
    if request.method == 'POST' and form.is_valid():
        application = form.save(commit=False)
        application.course = course
        application.save()
        form_success = True
        form = CourseApplicationForm()
    
    context = {
        'page_title': f'{course.name} - Course Details',
        'course': course,
        'related_courses': related_courses,
        'application_form': form,
        'form_success': form_success,
    }
    return render(request, 'core/course_detail.html', context)


def contact(request):
    context = {
        'page_title': 'Contact',
    }
    return render(request, 'accounts/contact_base.html', context)


def caravan_list(request):
    """Display list of available caravans with search and filtering"""
    from .forms import CaravanSearchForm
    from .models import Caravan
    
    caravans_list = Caravan.objects.filter(is_active=True, is_available=True).order_by('name')
    
    # Handle search form
    form = CaravanSearchForm(request.GET or None)
    if form.is_valid():
        # Filter by caravan type
        if form.cleaned_data.get('caravan_type'):
            caravans_list = caravans_list.filter(caravan_type=form.cleaned_data['caravan_type'])
        
        # Filter by capacity
        if form.cleaned_data.get('capacity'):
            capacity = int(form.cleaned_data['capacity'])
            caravans_list = caravans_list.filter(capacity__gte=capacity)
        
        # Filter by price range
        if form.cleaned_data.get('price_range'):
            price_range = form.cleaned_data['price_range']
            if price_range == '1000-3000':
                caravans_list = caravans_list.filter(daily_rate__gte=1000, daily_rate__lte=3000)
            elif price_range == '3000-5000':
                caravans_list = caravans_list.filter(daily_rate__gte=3000, daily_rate__lte=5000)
            elif price_range == '5000-8000':
                caravans_list = caravans_list.filter(daily_rate__gte=5000, daily_rate__lte=8000)
            elif price_range == '8000+':
                caravans_list = caravans_list.filter(daily_rate__gte=8000)
        
        # Filter by amenities
        if form.cleaned_data.get('has_ac'):
            caravans_list = caravans_list.filter(has_ac=True)
        if form.cleaned_data.get('has_kitchen'):
            caravans_list = caravans_list.filter(has_kitchen=True)
        if form.cleaned_data.get('has_bathroom'):
            caravans_list = caravans_list.filter(has_bathroom=True)
    
    # Get featured caravans
    featured_caravans = Caravan.objects.filter(is_active=True, is_available=True, is_featured=True)[:3]
    
    # Pagination
    paginator = Paginator(caravans_list, 9)
    page = request.GET.get('page')
    
    try:
        caravans = paginator.page(page)
    except PageNotAnInteger:
        caravans = paginator.page(1)
    except EmptyPage:
        caravans = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': 'Caravan Rentals',
        'caravans': caravans,
        'featured_caravans': featured_caravans,
        'form': form,
        'caravan_types': Caravan.CARAVAN_TYPES,
    }
    return render(request, 'core/caravan_list.html', context)


def caravan_detail(request, slug):
    """Display detailed information about a specific caravan"""
    from .models import Caravan
    from .forms import CaravanBookingForm
    
    caravan = get_object_or_404(Caravan, slug=slug, is_active=True)
    
    # Get related caravans (same type)
    related_caravans = Caravan.objects.filter(
        is_active=True,
        is_available=True,
        caravan_type=caravan.caravan_type
    ).exclude(id=caravan.id)[:3]
    
    # Handle booking form
    form = CaravanBookingForm(request.POST or None)
    form_success = False
    
    if request.method == 'POST' and form.is_valid():
        if request.user.is_authenticated:
            booking = form.save(commit=False)
            booking.caravan = caravan
            booking.user = request.user
            
            # Calculate total amount based on duration
            from datetime import date
            pickup_date = form.cleaned_data['pickup_date']
            return_date = form.cleaned_data['return_date']
            duration_days = (return_date - pickup_date).days
            
            if duration_days >= 7:
                # Weekly rate for 7+ days
                total_amount = (duration_days // 7) * caravan.weekly_rate
                remaining_days = duration_days % 7
                if remaining_days > 0:
                    total_amount += remaining_days * caravan.daily_rate
            else:
                # Daily rate for less than 7 days
                total_amount = duration_days * caravan.daily_rate
            
            booking.total_amount = total_amount
            booking.save()
            form_success = True
            form = CaravanBookingForm()
        else:
            # Redirect to login if user is not authenticated
            from django.contrib.auth.decorators import login_required
            return redirect('accounts:login')
    
    context = {
        'page_title': f'{caravan.name} - Caravan Details',
        'caravan': caravan,
        'related_caravans': related_caravans,
        'booking_form': form,
        'form_success': form_success,
    }
    return render(request, 'core/caravan_detail.html', context)

def search_destinations(request):
    query = request.GET.get('q', '')
    
    if query:
        destinations = Destination.objects.filter(
            Q(name__icontains=query) | 
            Q(location__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query),
            is_active=True
        ).distinct().order_by('name')
    else:
        destinations = Destination.objects.filter(is_active=True).order_by('name')
    
    context = {
        'destinations': destinations,
        'search_query': query,
        'page_title': f'Search Results for "{query}"',
    }
    
    return render(request, 'core/search_results.html', context)

# Filter destinations by category
def destinations_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    
    destinations = Destination.objects.filter(
        tags__name__icontains=category.name,  # Using tags to simulate categories
        is_active=True
    ).distinct().order_by('name')
    
    context = {
        'destinations': destinations,
        'category': category,
        'page_title': f'Destinations in {category.name}',
    }
    
    return render(request, 'core/destinations_by_category.html', context)

# Filter destinations by type
def destinations_by_type(request, destination_type):
    # Validate destination type
    valid_types = [choice[0] for choice in Destination.DESTINATION_TYPES]
    if destination_type not in valid_types:
        destinations = Destination.objects.none()
    else:
        destinations = Destination.objects.filter(
            destination_type=destination_type,
            is_active=True
        ).order_by('name')
    
    # Get display name for the type
    type_display = dict(Destination.DESTINATION_TYPES).get(destination_type, destination_type)
    
    context = {
        'destinations': destinations,
        'destination_type': destination_type,
        'type_display': type_display,
        'page_title': f'{type_display} Destinations',
    }
    
    return render(request, 'core/destinations_by_type.html', context)
from django.contrib import admin
from .models import Destination, DestinationImage, Testimonial, Tag, Category, PointOfInterest, Course, CourseApplication, Exam, Caravan, CaravanBooking

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ['image', 'caption', 'is_primary']

class PointOfInterestInline(admin.TabularInline):
    model = PointOfInterest
    extra = 1
    fields = ['name', 'x_percent', 'y_percent', 'latitude', 'longitude', 'google_place_id', 'icon', 'description']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'price_per_person', 'destination_type', 'is_active', 'is_featured']
    list_filter = ['destination_type', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'location', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DestinationImageInline, PointOfInterestInline]
    filter_horizontal = ['tags']

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ['destination', 'caption', 'is_primary']
    list_filter = ['destination', 'is_primary']
    search_fields = ['destination__name', 'caption']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'destination', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'feedback', 'destination__name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'x_percent', 'y_percent']
    list_filter = ['destination']
    search_fields = ['name', 'destination__name']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'duration_weeks', 'max_students', 'is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'short_description']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'category', 'featured_image')
        }),
        ('Course Details', {
            'fields': ('price', 'duration_weeks', 'max_students', 'start_date')
        }),
        ('Content', {
            'fields': ('syllabus', 'requirements', 'benefits')
        }),
        ('Settings', {
            'fields': ('is_active', 'is_featured')
        }),
    )

@admin.register(CourseApplication)
class CourseApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'course', 'email', 'status', 'created_at']
    list_filter = ['course', 'status', 'created_at']
    search_fields = ['full_name', 'email', 'message']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'scheduled_at', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']


@admin.register(Caravan)
class CaravanAdmin(admin.ModelAdmin):
    list_display = ['name', 'caravan_type', 'capacity', 'daily_rate', 'is_available', 'is_featured', 'created_at']
    list_filter = ['caravan_type', 'is_available', 'is_featured', 'fuel_type', 'transmission', 'year']
    search_fields = ['name', 'description', 'pickup_locations']
    list_editable = ['is_available', 'is_featured']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'caravan_type', 'description', 'short_description')
        }),
        ('Capacity & Features', {
            'fields': ('capacity', 'beds', 'has_ac', 'has_kitchen', 'has_bathroom', 'has_generator')
        }),
        ('Vehicle Specifications', {
            'fields': ('fuel_type', 'transmission', 'mileage', 'year')
        }),
        ('Pricing', {
            'fields': ('daily_rate', 'weekly_rate', 'security_deposit')
        }),
        ('Images', {
            'fields': ('featured_image', 'interior_image', 'exterior_image')
        }),
        ('Availability & Location', {
            'fields': ('is_available', 'pickup_locations', 'max_distance')
        }),
        ('Additional Info', {
            'fields': ('amenities', 'rules', 'insurance_info')
        }),
        ('Metadata', {
            'fields': ('is_featured', 'is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(CaravanBooking)
class CaravanBookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'caravan', 'user', 'full_name', 'pickup_date', 'return_date', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'pickup_date', 'return_date', 'caravan__caravan_type']
    search_fields = ['full_name', 'email', 'phone', 'caravan__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    
    fieldsets = (
        ('Booking Details', {
            'fields': ('caravan', 'user', 'pickup_date', 'return_date', 'pickup_location', 'return_location')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone', 'driving_license')
        }),
        ('Trip Details', {
            'fields': ('destination', 'purpose', 'special_requirements')
        }),
        ('Financial', {
            'fields': ('total_amount', 'security_deposit_paid')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('caravan', 'user')
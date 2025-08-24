from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Destination(models.Model):
    DESTINATION_TYPES = [
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('historical', 'Historical'),
        ('wildlife', 'Wildlife'),
        ('religious', 'Religious'),
        ('cultural', 'Cultural'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=200)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    image = models.ImageField(upload_to='destinations/')
    map_image = models.ImageField(upload_to='maps/', blank=True, null=True)
    destination_type = models.CharField(max_length=20, choices=DESTINATION_TYPES)
    
    # Amenities
    shower_count = models.PositiveIntegerField(default=1)
    bed_count = models.PositiveIntegerField(default=1)
    near_mountain = models.BooleanField(default=False)
    near_beach = models.BooleanField(default=False)
    
    # Metadata
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Tags for better search
    tags = models.ManyToManyField('Tag', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('destination_detail', kwargs={'slug': self.slug})
    
    @property
    def gallery_images(self):
        """Get all gallery images for this destination"""
        return self.images.all()

class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination, 
        on_delete=models.CASCADE, 
        related_name='images'  # Changed from default to avoid clash
    )
    image = models.ImageField(upload_to='destination_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.destination.name}"


class PointOfInterest(models.Model):
    """Clickable points placed over a destination's mini-map image.

    x_percent and y_percent are percentages (0-100) relative to the map image size,
    used for absolutely positioning markers over the image in the UI.
    """
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='points_of_interest'
    )
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    # Position on the image (0-100)
    x_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text='Left position in % (0-100)')
    y_percent = models.DecimalField(max_digits=5, decimal_places=2, help_text='Top position in % (0-100)')
    # Optional visual for marker/thumbnail
    icon = models.ImageField(upload_to='poi_icons/', blank=True, null=True)
    # Coordinates for Google Maps deep link
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    google_place_id = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = 'Point of Interest'
        verbose_name_plural = 'Points of Interest'

    def __str__(self):
        return f"{self.name} ({self.destination.name})"

    @property
    def google_maps_url(self) -> str:
        if self.google_place_id:
            return f"https://www.google.com/maps/place/?q=place_id:{self.google_place_id}"
        if self.latitude is not None and self.longitude is not None:
            return f"https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}"
        # Fallback: search by name near destination location
        return f"https://www.google.com/maps/search/?api=1&query={self.name} {self.destination.location}"

class Testimonial(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    feedback = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    destination = models.ForeignKey(
        Destination, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='testimonials'  # Added related_name to avoid potential clashes
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial by {self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Course(models.Model):
    COURSE_CATEGORIES = [
        ('tourism', 'Tourism & Hospitality'),
        ('guide', 'Tour Guide'),
        ('management', 'Tourism Management'),
        ('culture', 'Cultural Studies'),
        ('language', 'Language Courses'),
        ('photography', 'Travel Photography'),
        ('cooking', 'Local Cuisine'),
        ('crafts', 'Traditional Crafts'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=20, choices=COURSE_CATEGORIES, default='tourism')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_weeks = models.PositiveIntegerField(help_text="Duration in weeks", default=4)
    max_students = models.PositiveIntegerField(default=20)
    start_date = models.DateField(blank=True, null=True)
    featured_image = models.ImageField(upload_to='courses/', blank=True, null=True)
    syllabus = models.TextField(blank=True, help_text="Course outline and topics covered")
    requirements = models.TextField(blank=True, help_text="Prerequisites and requirements")
    benefits = models.TextField(blank=True, help_text="What students will gain from this course")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    @property
    def formatted_price(self):
        return f"₹{self.price:,.2f}"
    
    @property
    def duration_text(self):
        if self.duration_weeks == 1:
            return "1 week"
        elif self.duration_weeks < 4:
            return f"{self.duration_weeks} weeks"
        else:
            months = self.duration_weeks // 4
            weeks = self.duration_weeks % 4
            if weeks == 0:
                return f"{months} month{'s' if months > 1 else ''}"
            else:
                return f"{months} month{'s' if months > 1 else ''} {weeks} week{'s' if weeks > 1 else ''}"


class CourseApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.course.name}"


class Exam(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)
    external_link = models.URLField(blank=True)
    attachment = models.FileField(upload_to='exams/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Caravan(models.Model):
    CARAVAN_TYPES = [
        ('luxury', 'Luxury Caravan'),
        ('adventure', 'Adventure Caravan'),
        ('family', 'Family Caravan'),
        ('eco', 'Eco-friendly Caravan'),
        ('compact', 'Compact Caravan'),
        ('premium', 'Premium Caravan'),
    ]
    
    FUEL_TYPES = [
        ('diesel', 'Diesel'),
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    TRANSMISSION_TYPES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    caravan_type = models.CharField(max_length=20, choices=CARAVAN_TYPES, default='family')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Capacity and Features
    capacity = models.PositiveIntegerField(help_text="Number of people it can accommodate")
    beds = models.PositiveIntegerField(default=2, help_text="Number of beds")
    has_ac = models.BooleanField(default=True, verbose_name="Air Conditioning")
    has_kitchen = models.BooleanField(default=True, verbose_name="Kitchen")
    has_bathroom = models.BooleanField(default=True, verbose_name="Bathroom")
    has_generator = models.BooleanField(default=True, verbose_name="Generator")
    
    # Vehicle Specifications
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES, default='diesel')
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_TYPES, default='manual')
    mileage = models.PositiveIntegerField(help_text="Average mileage per liter")
    year = models.PositiveIntegerField(help_text="Manufacturing year")
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Daily rental rate")
    weekly_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Weekly rental rate (discounted)")
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2, help_text="Security deposit required")
    
    # Images
    featured_image = models.ImageField(upload_to='caravans/', blank=True, null=True)
    interior_image = models.ImageField(upload_to='caravans/interior/', blank=True, null=True)
    exterior_image = models.ImageField(upload_to='caravans/exterior/', blank=True, null=True)
    
    # Availability and Location
    is_available = models.BooleanField(default=True)
    pickup_locations = models.TextField(help_text="Available pickup locations")
    max_distance = models.PositiveIntegerField(help_text="Maximum travel distance allowed (km)")
    
    # Additional Info
    amenities = models.TextField(blank=True, help_text="Additional amenities and features")
    rules = models.TextField(blank=True, help_text="Rental rules and restrictions")
    insurance_info = models.TextField(blank=True, help_text="Insurance coverage details")
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({self.get_caravan_type_display()})"
    
    def get_absolute_url(self):
        return reverse('caravan_detail', kwargs={'slug': self.slug})
    
    @property
    def formatted_daily_rate(self):
        return f"₹{self.daily_rate:,.0f}"
    
    @property
    def formatted_weekly_rate(self):
        return f"₹{self.weekly_rate:,.0f}"
    
    @property
    def weekly_discount(self):
        """Calculate discount percentage for weekly rental"""
        if self.daily_rate > 0:
            weekly_daily_total = self.daily_rate * 7
            discount = ((weekly_daily_total - self.weekly_rate) / weekly_daily_total) * 100
            return round(discount, 1)
        return 0
    
    @property
    def is_eco_friendly(self):
        return self.caravan_type == 'eco' or self.fuel_type == 'electric'


class CaravanBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    caravan = models.ForeignKey(Caravan, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='caravan_bookings')
    
    # Booking Details
    pickup_date = models.DateField()
    return_date = models.DateField()
    pickup_location = models.CharField(max_length=200)
    return_location = models.CharField(max_length=200, blank=True, help_text="Leave blank if same as pickup")
    
    # Customer Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    driving_license = models.CharField(max_length=50, help_text="Driving License Number")
    
    # Trip Details
    destination = models.CharField(max_length=200, blank=True, help_text="Main destination for the trip")
    purpose = models.CharField(max_length=100, blank=True, help_text="Purpose of trip (leisure, business, etc.)")
    special_requirements = models.TextField(blank=True, help_text="Any special requirements or requests")
    
    # Pricing
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit_paid = models.BooleanField(default=False)
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.caravan.name} ({self.pickup_date} to {self.return_date})"
    
    @property
    def duration_days(self):
        """Calculate duration of booking in days"""
        return (self.return_date - self.pickup_date).days
    
    @property
    def is_active_booking(self):
        """Check if booking is currently active"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.pickup_date <= today <= self.return_date and self.status == 'confirmed'
from django import forms
from .models import CourseApplication, Testimonial, Caravan, CaravanBooking
from agency.models import Agency

class SearchForm(forms.Form):
    destination = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search place',
            'class': 'form-control'
        })
    )

class CourseApplicationForm(forms.ModelForm):
    class Meta:
        model = CourseApplication
        fields = ['full_name', 'email', 'phone', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Phone Number (Optional)'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us why you want to join this course...'
            }),
        }

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with West Bengal Tourism...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class CaravanSearchForm(forms.Form):
    caravan_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Caravan.CARAVAN_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    capacity = forms.ChoiceField(
        choices=[
            ('', 'Any Capacity'),
            ('2', '2 People'),
            ('4', '4 People'),
            ('6', '6 People'),
            ('8', '8+ People')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    price_range = forms.ChoiceField(
        choices=[
            ('', 'Any Price'),
            ('1000-3000', '₹1,000 - ₹3,000'),
            ('3000-5000', '₹3,000 - ₹5,000'),
            ('5000-8000', '₹5,000 - ₹8,000'),
            ('8000+', '₹8,000+')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    has_ac = forms.BooleanField(required=False, label='Air Conditioning')
    has_kitchen = forms.BooleanField(required=False, label='Kitchen')
    has_bathroom = forms.BooleanField(required=False, label='Bathroom')
    pickup_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    return_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class CaravanBookingForm(forms.ModelForm):
    class Meta:
        model = CaravanBooking
        fields = [
            'pickup_date', 'return_date', 'pickup_location', 'return_location',
            'full_name', 'email', 'phone', 'driving_license',
            'destination', 'purpose', 'special_requirements'
        ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': 'today'
            }),
            'return_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': 'today'
            }),
            'pickup_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Pickup location'
            }),
            'return_location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Return location (optional)'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your phone number'
            }),
            'driving_license': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Driving license number'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Main destination for your trip'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Purpose of trip (leisure, business, etc.)'
            }),
            'special_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special requirements or requests'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        pickup_date = cleaned_data.get('pickup_date')
        return_date = cleaned_data.get('return_date')
        
        if pickup_date and return_date:
            if pickup_date >= return_date:
                raise forms.ValidationError("Return date must be after pickup date")
            
            from datetime import date
            if pickup_date < date.today():
                raise forms.ValidationError("Pickup date cannot be in the past")
        
        return cleaned_data

class AgencyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['name', 'owner_name', 'email', 'phone', 'website', 'address', 'city', 'state', 'country', 'description', 'logo', 'license_document']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agency Name'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Owner/Manager Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Official Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your agency, services, experience'}),
        }
    
    checkin = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Check In Date',
            'class': 'form-control checkin_date'
        })
    )
    
    checkout = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Check Out Date',
            'class': 'form-control checkout_date'
        })
    )
    
    price_limit = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Select Price Limit'),
            ('5000', '$5,000'),
            ('10000', '$10,000'),
            ('50000', '$50,000'),
            ('100000', '$100,000'),
            ('200000', '$200,000'),
            ('300000', '$300,000'),
            ('400000', '$400,000'),
            ('500000', '$500,000'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
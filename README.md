# West Bengal Tourism

## Overview
This Django project includes a complete authentication system with user registration, login, and logout functionality.

## Features

### User Registration (Sign Up)
- Username, email, and full name required
- Age field (optional)
- Password confirmation
- Automatic login after successful registration
- Email uniqueness validation

### User Login
- Username and password authentication
- Remember next URL parameter for redirects
- User-friendly error messages
- Automatic redirect if already logged in

### User Logout
- Secure logout functionality
- Success message confirmation
- Redirect to home page

## Technical Details

### URLs
- **Sign Up**: `/accounts/signup/`
- **Login**: `/accounts/login/`
- **Logout**: `/accounts/logout/`

### Views
- `signup_view`: Handles user registration
- `login_view`: Handles user authentication
- `logout_view`: Handles user logout (requires login)

### Forms
- `SignUpForm`: Extends Django's UserCreationForm
- `LoginForm`: Simple username/password form

### Models
- `UserProfile`: Extended user profile with age field
- Automatically created when user registers

## Settings Configuration
The following authentication settings are configured in `tourism/settings.py`:

```python
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'
```

## Styling
Custom CSS has been added to `static/css/style.css` for:
- Form styling and animations
- Alert message styling
- Responsive design
- Modern UI elements

## Testing
Run the authentication tests with:
```bash
python manage.py test accounts
```

## Usage Examples

### Creating a Test User
```bash
python manage.py createsuperuser --username testuser --email test@example.com --noinput
python manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='testuser'); u.set_password('testpass123'); u.save()"
```

### Running the Development Server
```bash
python manage.py runserver
```

## Security Features
- CSRF protection enabled
- Password validation using Django's built-in validators
- Session-based authentication
- Secure password hashing
- Form validation and sanitization

## Browser Support
- Modern browsers with CSS3 and JavaScript support
- Responsive design for mobile and desktop
- Bootstrap 4.5.0 framework

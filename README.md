# Bengal Tourism

## Overview
This Django project provides a comprehensive platform for exploring the beautiful destinations of West Bengal. It includes features for user authentication, destination listings, and various travel-related services.

## Features
- **User Authentication**: Sign up, login, and logout functionalities.
- **Destination Listings**: Explore various destinations categorized by type (beach, mountain, historical, etc.).
- **Detailed Views**: Get detailed information about each destination, including images and descriptions.
- **Search Functionality**: Search for destinations based on user preferences.
- **Caravan Rentals**: Browse and book caravans for travel.
- **Courses**: Enroll in various courses related to tourism and hospitality.
- **Contact and Support**: Reach out for inquiries and support.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd tourism
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project
1. Apply migrations:
   ```bash
   python manage.py migrate
   ```
2. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```
4. Access the application at `http://127.0.0.1:8000/`.

## Directory Structure
```
tourism/
│
├── accounts/               # User authentication
├── agency/                 # Agency-related functionalities
├── core/                   # Core application logic
├── media/                  # Uploaded media files
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
└── manage.py               # Django management script
```

## Testing
Run the tests for the application:
```bash
python manage.py test
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Django framework for web development.
- Bootstrap for responsive design.
- Various contributors and resources that helped in the development of this project.

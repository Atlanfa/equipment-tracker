# Equipment Tracking Project

This project is a Django web application designed for tracking equipment quality control (QC). It provides a user-friendly interface for managing equipment entries, including their QC status and repair information.

## Project Structure

The project is organized as follows:

```
equipment_tracking_project/
├── equipment_tracking_app/          # Main application directory
│   ├── migrations/                  # Database migrations
│   ├── static/                      # Static files (CSS, JS, etc.)
│   ├── templates/                   # HTML templates
│   ├── __init__.py                  # Marks the directory as a Python package
│   ├── admin.py                     # Admin site configuration
│   ├── apps.py                      # Application configuration
│   ├── models.py                    # Data models
│   ├── tests.py                     # Application tests
│   └── views.py                     # View functions
├── equipment_tracking_project/       # Project configuration directory
│   ├── __init__.py                  # Marks the directory as a Python package
│   ├── asgi.py                      # ASGI configuration
│   ├── settings.py                  # Project settings
│   ├── urls.py                      # URL routing
│   └── wsgi.py                      # WSGI configuration
├── manage.py                        # Command-line utility for the project
└── README.md                        # Project documentation
```

## Features

- **User Interface**: A responsive web interface for tracking equipment QC.
- **Filtering and Searching**: Users can filter and search through equipment entries based on various criteria.
- **Dark Mode**: A toggle for switching between light and dark themes.
- **Notes Section**: Users can add notes related to equipment, with highlighting capabilities.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd equipment_tracking_project
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```
   python manage.py migrate
   ```

5. Start the development server:
   ```
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Navigate through the application to track equipment QC.
- Use the filtering options to narrow down the entries.
- Add notes and highlight relevant equipment as needed.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
# Web Scraper Application

## Project Structure
This project follows a modular design pattern where each component has its own responsibility:

```
project_root/
│-- main.py                # Entry point for the application
│-- app/
│   │-- web_scraper_app.py # Main application class that coordinates everything
│   │-- ui/                # Contains UI components (scraper tab and downloader tab)
│   │-- core/              # Contains core business logic (scraper and downloader)
```

## How Components Are Linked
The components are linked together through:

- **Dependency Injection**: The `WebScraperApp` class instantiates and connects the UI and core components.
- **Callbacks**: UI components call methods in the main app class via callback functions.
- **Event Handlers**: The main app class handles events from the UI components and delegates to the core components.

## Installation & Usage
### Prerequisites
Make sure all files are placed in the correct directory structure and install the required dependencies:

```bash
pip install selenium requests
```

### Running the Application
```bash
python main.py
```

## Benefits of This Structure
- **Separation of Concerns**: UI, business logic, and application control are all separated.
- **Maintainability**: Each component handles a specific responsibility, making bug fixes and feature additions easier.
- **Testability**: Components can be tested in isolation.
- **Reusability**: Core components could be used in other applications or through different interfaces.

This modular structure ensures the code remains maintainable and scalable, allowing for easy extension with new features such as additional scraping methods or a settings panel without affecting the existing functionality.


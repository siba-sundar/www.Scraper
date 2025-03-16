# Web Scraper Application

## Project Structure
The structure follows a modular design pattern where each component has its own responsibility:

```
project-root/
│-- main.py                 # Entry point for the application
│-- requirements.txt        # Dependencies for installation
│-- app/
│   │-- web_scraper_app.py  # Main application class that coordinates everything
│   │-- ui/                 # Contains UI components (scraper tab and downloader tab)
│   │-- core/               # Contains core business logic (scraper and downloader)
```

## How Everything is Linked Together
The components are linked together through:

- **Dependency Injection:** The `WebScraperApp` class instantiates and connects the UI and core components.
- **Callbacks:** UI components call methods in the main app class via callback functions.
- **Event Handlers:** The main app class handles events from the UI components and delegates to the core components.

## Installation & Usage
### 1. Install Required Dependencies
Ensure you have Python installed, then install dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 2. Run the Application
After installing dependencies, start the application with:

```bash
python main.py
```

## Benefits of This Structure
- **Separation of Concerns:** UI, business logic, and application control are all separated.
- **Maintainability:** Each component handles a specific responsibility, making bug fixes and feature additions easier.
- **Testability:** Components can be tested in isolation.
- **Reusability:** Core components could be used in other applications or through different interfaces.

This modular structure makes your code more maintainable and easier to extend with new features. For example, you could easily add more tabs for different scraping methods or a settings panel without affecting existing functionality.


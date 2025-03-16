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

## Features

### Scraper Tab Features:

- Input fields for the website URL, element selector, and selector type (class, id, tag, CSS selector, or XPath).
- Option to choose between image or text content extraction.
- Dynamic configuration fields based on content type:
  - **For images:** ID attribute, title selector, and image selector fields.
  - **For text:** ID/name selector, title selector, and content selector fields.
- Output JSON file selection with a browse button.
- Wait time adjustment for page loading.
- Headless browser option.
- Detailed console output with progress tracking.

### Downloader Tab Features:

- JSON file selection with a browse button.
- Output folder selection with a browse button.
- Delay setting between downloads.
- Detailed console output with progress tracking.

### Key Functionality:

- **Automated Workflow:** After scraping images, it auto-fills the downloader tab and switches to it.
- **Progress Tracking:** Visual progress bar and status messages.
- **Error Handling:** Comprehensive error handling for all operations.
- **Threading:** Background processing to keep the UI responsive.
- **Smart Filename Generation:** Creates safe filenames with proper extensions.

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

## How to Use

### For Image Scraping:

1. Enter the website URL.
2. Specify the element selector (like "SearchResultImageItem").
3. Choose selector type.
4. Enter prefered file location and esxtract the data.
5. Select the prefered location to download and download the extracted data.

This modular structure makes your code more maintainable and easier to extend with new features. For example, you could easily add more tabs for different scraping methods or a settings panel without affecting existing functionality.


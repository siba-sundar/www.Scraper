import tkinter as tk
from app.web_scraper_app import WebScraperApp

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
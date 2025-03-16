import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

class WebScraper:
    def __init__(self, logger, progress_updater, status_updater):
        self.logger = logger
        self.update_progress = progress_updater
        self.update_status = status_updater
        
    def scrape(self, url, selector, selector_type, content_type, output_file, wait_time, headless, 
               extraction_config):
        self.logger(f"Starting to scrape: {url}")
        self.update_status("Scraping in progress...")
        self.update_progress(10)
        
        # Setup Chrome options
        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--incognito")
        
        driver = None
        try:
            # Initialize WebDriver
            self.logger("Initializing browser...")
            driver = webdriver.Chrome(options=chrome_options)
            
            # Visit the URL
            self.logger(f"Visiting URL: {url}")
            driver.get(url)
            
            # Wait for the page to load
            self.logger(f"Waiting {wait_time} seconds for page to load...")
            time.sleep(wait_time)
            
            # Select elements based on selector type
            self.logger(f"Looking for elements with {selector_type}: {selector}")
            elements = self._find_elements(driver, selector_type, selector)
                
            if not elements:
                self.logger("No elements found with the given selector.")
                self.update_status("No elements found")
                self.update_progress(0)
                return None, None
                
            self.logger(f"Found {len(elements)} elements")
            self.update_progress(30)
            
            # Extract data based on content type
            data = []
            
            if content_type == "image":
                data = self._extract_image_data(elements, extraction_config)
            else:
                data = self._extract_text_data(elements, extraction_config)
                        
            # Save data to JSON file
            self.update_progress(90)
            self.logger(f"Saving data to {output_file}...")
            
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.logger(f"Successfully saved {len(data)} items to {output_file}")
            except Exception as e:
                self.logger(f"Error saving JSON file: {str(e)}")
                return None, None
                
            self.update_status("Scraping completed")
            self.update_progress(100)
            return output_file, data
            
        except Exception as e:
            self.logger(f"Error during scraping: {str(e)}")
            self.update_status("Error occurred")
            self.update_progress(0)
            return None, None
        finally:
            if driver:
                driver.quit()
                self.logger("Browser closed")
    
    def _find_elements(self, driver, selector_type, selector):
        elements = []
        try:
            if selector_type == "class":
                elements = driver.find_elements(By.CLASS_NAME, selector)
            elif selector_type == "id":
                elements = [driver.find_element(By.ID, selector)]
            elif selector_type == "tag":
                elements = driver.find_elements(By.TAG_NAME, selector)
            elif selector_type == "css_selector":
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            elif selector_type == "xpath":
                elements = driver.find_elements(By.XPATH, selector)
        except Exception as e:
            self.logger(f"Error finding elements: {str(e)}")
            elements = []
        return elements
        
    def _extract_image_data(self, elements, config):
        id_attr = config.get("id_attr", "")
        title_selector = config.get("title_selector", "")
        img_selector = config.get("img_selector", "")
        
        data = []
        self.logger("Extracting image data...")
        
        for i, elem in enumerate(elements):
            self.update_progress(30 + (50 * i / len(elements)))
            
            try:
                # Extract image ID from the data attribute
                image_id = elem.get_attribute(id_attr) if id_attr else f"img_{i}"
                
                # Get image title
                try:
                    image_title = elem.find_element(By.CSS_SELECTOR, title_selector).get_attribute("title")
                except:
                    try:
                        image_title = elem.find_element(By.CSS_SELECTOR, title_selector).text
                    except:
                        image_title = f"image_{i}"
                        
                # Get image source
                try:
                    image_src = elem.find_element(By.CSS_SELECTOR, img_selector).get_attribute("src")
                except:
                    image_src = "not_found"
                    
                data.append({
                    "id": image_id,
                    "title": image_title,
                    "src": image_src
                })
                
                self.logger(f"Processed image {i+1}/{len(elements)}: {image_title}")
            except Exception as e:
                self.logger(f"Error processing element {i+1}: {str(e)}")
                
        return data
        
    def _extract_text_data(self, elements, config):
        id_selector = config.get("id_selector", "")
        title_selector = config.get("title_selector", "")
        content_selector = config.get("content_selector", "")
        
        data = []
        self.logger("Extracting text data...")
        
        for i, elem in enumerate(elements):
            self.update_progress(30 + (50 * i / len(elements)))
            
            try:
                # Extract ID/name
                try:
                    item_id = elem.find_element(By.CSS_SELECTOR, id_selector).text if id_selector else f"item_{i}"
                except:
                    item_id = f"item_{i}"
                    
                # Get title
                try:
                    item_title = elem.find_element(By.CSS_SELECTOR, title_selector).text if title_selector else ""
                except:
                    item_title = ""
                    
                # Get content
                try:
                    item_content = elem.find_element(By.CSS_SELECTOR, content_selector).text if content_selector else elem.text
                except:
                    item_content = elem.text
                    
                data.append({
                    "id": item_id,
                    "title": item_title,
                    "content": item_content
                })
                
                self.logger(f"Processed item {i+1}/{len(elements)}: {item_title if item_title else item_id}")
            except Exception as e:
                self.logger(f"Error processing element {i+1}: {str(e)}")
                
        return data
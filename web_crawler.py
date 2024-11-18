import csv
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the Edge driver
driver_path = r"C:\Users\Lenovo\Downloads\edgedriver_win64\msedgedriver.exe"
service = EdgeService(executable_path=driver_path)
driver = webdriver.Edge(service=service)

# Open the Google AI blog page
driver.get("https://blog.google/technology/ai/")

# Wait for the articles to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.uni-nup__card"))
)

# Find all article elements
articles = driver.find_elements(By.CSS_SELECTOR, "div.uni-nup__card")

# Extract titles and links
article_info = []
for article in articles:
    title_element = article.find_element(By.CSS_SELECTOR, "h3.uni-nup__header")
    link_element = article.find_element(By.CSS_SELECTOR, "a")

    title = title_element.text.strip()
    link = link_element.get_attribute("href").strip()

    article_info.append((title, link))

# Open each link, fetch article content, and save to CSV
with open("google_ai_articles.csv", mode="w", newline="", encoding="utf-8") as file:
    csv_writer = csv.writer(file)
    # Write header
    csv_writer.writerow(["Title", "Link", "Content"])

    for title, link in article_info:
        print(f"Title: {title}")
        print(f"Link: {link}")
        
        # Open the article page
        driver.get(link)
        
        # Wait for the article content to load
        try:
            article_content = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.module--text.module--text__article"))
            )
            # Extract the text content
            paragraphs = article_content.find_elements(By.CSS_SELECTOR, "p")
            content = "\n".join(paragraph.text.strip() for paragraph in paragraphs)
            
            print("Article Content:")
            print(content)
            
            # Save to CSV
            csv_writer.writerow([title, link, content])
        except Exception as e:
            print(f"Could not fetch article content for {title}: {e}")
            csv_writer.writerow([title, link, "Content not available"])
        
        print("\n" + "-"*80 + "\n")
        
        # Optional: Wait before navigating to the next link
        time.sleep(2)

# Close the driver
driver.quit()

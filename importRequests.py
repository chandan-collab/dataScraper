# import requests
# from bs4 import BeautifulSoup

# 1. Define the URL of the target website
# url = "https://www.kashiit.ac.in/"

# /*
# # 2. Fetch the HTML content of the page
# try:
#     response = requests.get(url)
#     response.raise_for_status()  # Raise an exception for bad status codes
#     html_content = response.text
# except requests.exceptions.RequestException as e:
#     print(f"Error fetching the URL: {e}")
#     exit()

# # 3. Parse the HTML content using Beautiful Soup
# soup = BeautifulSoup(html_content, 'html.parser')

# # 4. Extract data (e.g., all links)
# links = soup.find_all('a')

# # 5. Print the extracted data
# print(f"Links found on {url}:")
# for link in links:
#     href = link.get('href')
#     if href:  # Ensure the 'href' attribute exists
#         print(href)

# # Example of finding a specific element by ID or class
# # You can also find elements by ID:
# # element_by_id = soup.find(id='some_id')
# # if element_by_id:
# #     print(f"\nElement with ID 'some_id': {element_by_id.text}")

# # Or by class:
# # elements_by_class = soup.find_all(class_='some_class')
# # if elements_by_class:
# #     print(f"\nElements with class 'some_class':")
# #     for element in elements_by_class:
# #         print(element.text) */
# */

# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# import json

# visited_links = set()

# def scrape_website(url, output_file="scraped_data2.jsonl", depth=1, max_depth=2):
#     """
#     url: starting website link
#     output_file: JSONL file to save scraped text
#     depth: current crawling depth
#     max_depth: how deep we should follow links
#     """
#     if depth > max_depth or url in visited_links:
#         return
    
#     visited_links.add(url)

#     try:
#         headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#             }
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # remove unwanted tags
#         for script in soup(["script", "style", "noscript"]):
#             script.extract()
        
#         text = soup.get_text(separator="\n")
#         text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])

#         # Save as JSONL format (one JSON per line)
#         record = {
#             "url": url,
#             "content": text
#         }
        
#         with open(output_file, "a", encoding="utf-8") as file:
#             file.write(json.dumps(record, ensure_ascii=False) + "\n")
        
#         print(f" Scraped: {url}")

#         # find internal links and scrape them recursively
#         base_domain = urlparse(url).netloc
#         for link in soup.find_all("a", href=True):
#             full_link = urljoin(url, link["href"])
#             if urlparse(full_link).netloc == base_domain:
#                 scrape_website(full_link, output_file, depth + 1, max_depth)

#     except Exception as e:
#         print(f" Error scraping {url}: {e}")


# # Example usage:
# if __name__ == "__main__":
#     start_url = input("Enter website URL: ")  # e.g. https://en.wikipedia.org/wiki/Python_(programming_language)
#     scrape_website(start_url, "scraped_data2.jsonl", max_depth=2)
#     print("\ Crawling complete! Data saved in scraped_data2.jsonl (JSONL format)")


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import textwrap

visited_links = set()

def chunk_text(text, max_length=500):
    """Split text into smaller chunks for Q&A pairs"""
    return textwrap.wrap(text, max_length, break_long_words=False, replace_whitespace=False)

def scrape_website(url, output_file="qa_dataset.jsonl", depth=1, max_depth=2):
    if depth > max_depth or url in visited_links:
        return
    
    visited_links.add(url)

    try:
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # remove unwanted tags
        for script in soup(["script", "style", "noscript"]):
            script.extract()
        
        text = soup.get_text(separator=" ")
        text = " ".join([line.strip() for line in text.splitlines() if line.strip()])
        
        # break into chunks
        chunks = chunk_text(text, max_length=500)
        
        with open(output_file, "a", encoding="utf-8") as file:
            for i, chunk in enumerate(chunks, start=1):
                qa_record = {
                    "url": url,
                    "question": f"What is explained in this part? (section {i})",
                    "answer": chunk
                }
                file.write(json.dumps(qa_record, ensure_ascii=False) + "\n")
        
        print(f" Scraped & Converted to QA: {url}")

        # find internal links
        base_domain = urlparse(url).netloc
        for link in soup.find_all("a", href=True):
            full_link = urljoin(url, link["href"])
            if urlparse(full_link).netloc == base_domain:
                scrape_website(full_link, output_file, depth + 1, max_depth)

    except Exception as e:
        print(f" Error scraping {url}: {e}")


# Example usage
if __name__ == "__main__":
    start_url = input("Enter website URL: ")  # e.g. https://en.wikipedia.org/wiki/Python_(programming_language)
    scrape_website(start_url, "qa_dataset.jsonl", max_depth=2)
    print("\n Crawling complete! QA training data saved in qa_dataset.jsonl")

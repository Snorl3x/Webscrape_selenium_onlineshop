#!/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def scrape_ibay_mobile_phones():
    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get('https://ibay.com.mv')

    sleep(3)  # Allow page to load

    try:
        # Locate search input and button
        input_search = driver.find_element(By.ID, 'q_kw')
        search_button = driver.find_element(By.CSS_SELECTOR, '.btn.waves-effect.left')

        # Perform search
        input_search.send_keys("mobile phones")
        sleep(1)
        search_button.click()
        
        sleep(3)  # Wait for search results to load
        
        # Find all product containers
        products = driver.find_elements(By.CSS_SELECTOR, '.latest-list-item')

        print(f"Found {len(products)} products.")

        # Iterate through each product and extract details
        for product in products:
            try:
                # Get product image URL
                image_element = product.find_element(By.CSS_SELECTOR, '.col.m3.s4 img')  # Get the <img> tag directly
                image_url = image_element.get_attribute('src')
                print(f"Image URL: {image_url}")

                # Get product title and href (URL)
                title_element = product.find_element(By.CSS_SELECTOR, '.col.m7.s8 h5 a')
                title = title_element.text  # Get the text (title of the product)
                product_url = title_element.get_attribute('href')  # Get the href (link to product)
                print(f"Title: {title}")
                print(f"Product URL: {product_url}")

                # Try to get the product price
                try:
                    price_element = product.find_element(By.CSS_SELECTOR, '.price')
                    price = price_element.text
                    print(f"Price: {price}")
                except Exception:
                    print("Price not found.")

            except Exception as e:
                print(f"Error scraping product: {e}")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

# Call the function
scrape_ibay_mobile_phones()

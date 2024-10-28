#!/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from time import sleep
import json

def defined():
    # Setup the Chrome WebDriver
    driver = webdriver.Chrome()

    # Navigate to the website
    driver.get('sitename')

    sleep(3)  # Allow page to load

    results = []  # List to hold the scraped data

    try:
        # Locate search input and button
        input_search = driver.find_element(By.ID, 'idclassname')
        search_button = driver.find_element(By.CSS_SELECTOR, 'btnclassname')

        # Perform search
        input_search.send_keys("mobile phones")
        sleep(1)
        search_button.click()

        sleep(3)  # Wait for search results to load

        # Loop for pagination
        while True:
            
            
            # Find all product containers
            products = driver.find_elements(By.CSS_SELECTOR, '.latest-list-item')
            print(f"Found {len(products)} products.")

            # Iterate through each product and extract details
            for product in products:
                try:
                    # Get product image URL
                    image_element = product.find_element(By.CSS_SELECTOR, '.imgclassname')
                    image_url = image_element.get_attribute('src')

                    # Get product title and href (URL)
                    title_element = product.find_element(By.CSS_SELECTOR, '.productclassname')
                    title = title_element.text
                    product_url = title_element.get_attribute('href')

                    # Try to get the product price
                    try:
                        price_element = product.find_element(By.CSS_SELECTOR, '.priceclassname')
                        price = price_element.text
                    except NoSuchElementException:
                        price = "Price not found."

                    # Append product details to results
                    results.append({
                        'title': title,
                        'url': product_url,
                        'image_url': image_url,
                        'price': price
                    })
                
                except Exception as e:
                    print(f"Error scraping product: {e}")

            # Try to click the "Next" button using XPath
            try:
                # Wait until the "Next" button is present and visible
                next_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@class='waves-effect']/a/i[contains(text(), 'navigate_next')]"))
                )

                # Scroll to the "Next" button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                sleep(1)

                # Click the "Next" button
                ActionChains(driver).move_to_element(next_button).click().perform()
                sleep(3)  # Wait for the next page to load

            except (NoSuchElementException, TimeoutException):
                print("No more pages to scrape or next button not found.")
                break  # Exit loop if the next button is not found

            except Exception as e:
                print(f"Error clicking the next button: {e}")
                break

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        driver.quit()

    # Save results to JSON file
    with open('nameyouwannasaveas', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print("File saved as JSON")

# Call the function
scrape_defined()

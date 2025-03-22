from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (optional)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument("--disable-3d-apis")  # Disable other GPU-related APIs

# Set a User-Agent string from a real browser
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36"
)

# Initialize the WebDriver (assuming ChromeDriver is in PATH)
driver = webdriver.Chrome(options=chrome_options)

# Open the NCAA stats website
driver.get("https://www.ncaa.com/stats/basketball-men/d1")

# Close Possible March Madness Pop-Up
try:
    mm_popup = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "bx-close-inside-2917691"))
    )
    mm_popup.click()
except:
    print("No Pop-Up")

# Iterate through each dropdown option and click it
iteration = 1
try:
    while True:
        # Re-find and expand the dropdown for each selection to avoid stale references
        stat_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "select-container-team-ps"))
        )
        stat_dropdown.click()

        # Get the dropdown options again after expanding
        dropdown_list = stat_dropdown.find_element(By.CLASS_NAME, "ps-results")
        dropdown_options = dropdown_list.find_elements(By.TAG_NAME, "li")

        option = dropdown_options[iteration]
        stat_name = option.text.strip()
        stat_value = option.get_attribute("data-val")

        if not stat_name or not stat_value:  # Skip empty options
            print(f"Skipping empty option: '{stat_name}'")
            iteration = iteration+1
            continue

        print(f"Clicking on: {stat_name}")

        # Scroll into view before clicking
        driver.execute_script("arguments[0].scrollIntoView();", option)
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(option)).click()

        #PAGER
        while True:
            try:
                next_page = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'stats-pager__li stats-pager__li--next')]/a"))
                )
                print("Clicking next page")
                next_page.click()
            except:
                print("no next page")
                break  # Stop if no next page is found

        iteration = iteration+1

except Exception as e:
    print("Error occurred while handling dropdown:", str(e))

# Close the driver after execution
driver.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-webgl")
chrome_options.add_argument("--disable-3d-apis")

# Set a User-Agent string from a real browser
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.100 Safari/537.36"
)

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the NCAA stats website
driver.get("https://www.ncaa.com/stats/basketball-men/d1")

# FCS
#driver.get("https://www.ncaa.com/stats/football/fcs")

# Close Possible March Madness Pop-Up
try:
    mm_popup = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, "bx-close-inside-2917691"))
    )
    mm_popup.click()
except:
    pass

# Iterate through each stat category in the dropdown
iteration = 1
try:
    while True:
        # Click the dropdown with the different stat categories
        # Since each stat is its own URL, the element needs to be re-identified each iteration
        stat_dropdown = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "select-container-team-ps"))
        )
        stat_dropdown.click()

        # Get the categories from the dropdown.
        dropdown_list = stat_dropdown.find_element(By.CLASS_NAME, "ps-results")
        dropdown_options = dropdown_list.find_elements(By.TAG_NAME, "li")

        option = dropdown_options[iteration]
        stat_name = option.text.strip()
        stat_value = option.get_attribute("data-val")

        if not stat_name or not stat_value: #Skip the dropdown title "option"
            iteration = iteration+1
            continue

        print(f"Selecting: {stat_name}")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(option)).click()

        # PAGER
        while True:
            try:
                next_page = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 'stats-pager__li stats-pager__li--next')]/a"))
                )
                next_page.click()
            except: # No more pages
                break

        iteration = iteration+1

except Exception as e:
    print("Error occurred while handling dropdown:", str(e))

driver.quit()
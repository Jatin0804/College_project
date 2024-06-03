from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# used to get the max years of data and its link
def get_max_years(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # get the initial address
    driver.get(url)

    range_element = driver.find_element(By.XPATH, '//*[@id="divRange"]/div/div[2]')
    range_years = range_element.find_elements(By.TAG_NAME, 'a')

    new_url = ""
    for r in range_years:
        href_ele = r.get_attribute('href')
        new_url = href_ele

    # Close the driver
    driver.quit()

    print(new_url)
    return new_url

if __name__ == "__main__":
    get_max_years("https://www.indexmundi.com/commodities/?commodity=agricultural-raw-materials-price-index")
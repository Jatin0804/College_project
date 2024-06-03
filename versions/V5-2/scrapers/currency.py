from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# used to get the max years of data and its link
def currency_url(url):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # get the initial address
    driver.get(url)

    temp = ""
    try:
        range_element = driver.find_element(By.XPATH, '//*[@id="frmCurrency"]')
        temp = "&currency=inr"
    except:
        pass

    new_url = url + temp

    # Close the driver
    driver.quit()

    print(new_url)
    return new_url

if __name__ == "__main__":
    # currency_url("https://www.indexmundi.com/commodities/?commodity=agricultural-raw-materials-price-index")
    currency_url("https://www.indexmundi.com/commodities/?commodity=sugar")
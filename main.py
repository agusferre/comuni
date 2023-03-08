from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import comuni_scraper as scraper

def main():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path=r'./chromedriver')
    try:
        scraper(driver)
    except:
        retry(driver)

def retry(driver):
    try:
        scraper(driver)
    except:
        retry(driver)

if __name__ == '__main__':
    main()
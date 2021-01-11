from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

SOGOU_URL = 'https://weixin.sogou.com/'
SEARCH_PATH = 'weixin?type=1&query='


def parse_weixin(public_name: str, title_name: str) -> str:
    options = Options()
    # options.add_argument('-headless')
    driver = Firefox(executable_path='/opt/portable/geckodriver',
                     options=options)
    wait = WebDriverWait(driver, timeout=10)
    driver.get(SOGOU_URL + SEARCH_PATH + public_name)
    wait.until(
        expected.visibility_of_element_located((
            By.CSS_SELECTOR,
            '#sogou_vr_11002301_box_0 > dl:nth-child(4) > dd:nth-child(2) > a:nth-child(1)'
        ))).click()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[-1])
    soup = BeautifulSoup(driver.page_source, features='lxml')
    content = soup.find(class_='rich_media_content')
    driver.quit()
    return content.text


if __name__ == "__main__":
    print(parse_weixin('腾讯玄武实验室'))

import time
import pyfiglet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BColors:
    OKCYAN = "\033[96m"
    WARNING = "\033[93m"


def main():
    driver = webdriver.Chrome()
    logger.debug("✨ Start Browser launched!")
    driver.get("https://engine.presearch.org/")

    input("Login and press [ENTER]: ")

    for line in open("files/terms.txt", "r").readlines():
        logger.debug("✨ Open the Presearch.org...")
        driver.get("https://www.presearch.org/?utm_source=extcr")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search")))
        logger.info(f"👾 Searching: {line}")
        element.send_keys(line, Keys.ENTER)
        time.sleep(10)

    driver.close()


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Auto Earn Pre-search")
    print(BColors.OKCYAN + ascii_banner)
    print(BColors.WARNING + "                   by @CI Monk\n")
    main()

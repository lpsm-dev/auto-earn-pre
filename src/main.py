# -*- coding: utf-8 -*-

# Import necessary libraries
import os
import time

# Import external libraries
import fire
import pyfiglet
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Import custom configuration module
from settings.config import Config

# Define a class to store color codes for formatting console outputs
class BColors:
    OKCYAN = "\033[96m"
    WARNING = "\033[93m"

# Initialize the configuration object
config = Config()

# Define the main function with an optional argument for the driver_type
def main(driver_type: str = "chrome"):
    """
    Main function to perform automated tasks on the Presearch.org website.
    :param driver_type: Type of WebDriver to use, 'chrome' or 'firefox'.
    :return: None
    """

    # Get the email and password from environment variables
    email = os.environ.get("PRESEARCH_EMAIL")
    password = os.environ.get("PRESEARCH_PASSWORD")

    # Configure the WebDriver based on the driver_type
    if driver_type == "chrome":
        logger.debug("✨ Using chromer driver")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
        )
        if config.get_env("CI") == "true":
            options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    if driver_type == "firefox":
        logger.debug("✨ Using firefox driver")
        service = FirefoxService(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-notifications")
        options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1"
        )
        if config.get_env("CI") == "true":
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=service, options=options)

    logger.debug("✨ Start Browser launched!")
    driver.get("https://presearch.org/")

    # Click on the "Register or Login" link to log in
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Register or Login')]"))
    )
    login_button.click()

    email_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[contains(@placeholder,'Email')]"))
    )
    email_field.click(email)

    password_field = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
    )
    password_field.click(password)

    # Wait for the user to enter the captcha and 2FA (two-factor authentication)
    input("Enter with the captcha + 2Auth and press [ENTER]: ")

    # Loop through the lines in the "files/terms.txt" file and perform search actions on Presearch.org
    for line in open("files/terms.txt", "r").readlines():
        logger.debug("✨ Open the Presearch.org...")
        driver.get("https://www.presearch.org/?utm_source=extcr")
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
        logger.info(f"👾 Searching {line.index}: {line}")
        element.send_keys(line, Keys.ENTER)
        time.sleep(10)

    # Close the WebDriver
    driver.close()

# Execute the main function when this script is run directly
if __name__ == "__main__":
    # Print the ASCII banner and additional information
    ascii_banner = pyfiglet.figlet_format("Auto Earn Pre-search")
    print(BColors.OKCYAN + ascii_banner)
    print(BColors.WARNING + "                   by @lpsm-dev\n")
    # Execute the main function using Fire CLI
    fire.Fire(main)

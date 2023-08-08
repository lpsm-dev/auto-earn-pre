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
from settings.constans import BColors

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
        logger.debug("Using chromer driver")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        if config.get_env("CI") == "true":
            options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    if driver_type == "firefox":
        logger.debug("Using firefox driver")
        service = FirefoxService(GeckoDriverManager().install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--disable-notifications")
        if config.get_env("CI") == "true":
            options.add_argument("--headless")
        driver = webdriver.Firefox(service=service, options=options)

    logger.debug("Start Browser launched!")
    driver.get("https://account.presearch.com/login")

    email_input = driver.find_element(By.XPATH, '//input[@name="email"]')
    email_input.send_keys(email)

    password_input = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_input.send_keys(password)

    # Click in "Remember Me" checkbox
    driver.find_element(By.XPATH, '//input[@name="remember"]').click()

    # Click in the captcha
    driver.find_element(By.XPATH, '//*[@id="login-form"]/form/div[3]/div[2]/div/iframe').click()

    # Wait for the user to resolve the captcha
    input("Resolve the captcha and press [ENTER]: ")

    # Click in Login button
    driver.find_element(By.XPATH, '//*[@id="login-form"]/form/div[3]/div[3]/button').click()

    # Wait for the user resolve the 2FA (two-factor authentication)
    input("Resolve the captcha + 2Auth and press [ENTER]: ")

    # Loop through the lines in the "files/terms.txt" file and perform search actions on Presearch.org
    for line in open(os.path.dirname(__file__) + "/files/terms.txt", "r").readlines():
        logger.info(f"Searching: {line}")
        driver.get("https://www.presearch.org")
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="q"]')))
        element.send_keys(line, Keys.ENTER)
        time.sleep(5)

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

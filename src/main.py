import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =======================================

def do_search(item):
	print("Open the Presearch.org ...")
	driver.get("https://www.presearch.org/?utm_source=extcr")
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "search")))
	print(f"Searching: {item}")
	element.send_keys(item, Keys.ENTER)
	time.sleep(10)

# =======================================

if __name__ == "__main__":
  driver = webdriver.Chrome()
  print("Browser launched")
  driver.get("https://engine.presearch.org/")

  input("Login and press [ENTER]")

  for line in open("search_terms.txt", "r").readlines():
    do_search(line)

  driver.close()

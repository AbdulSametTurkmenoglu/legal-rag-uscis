import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
import urllib.robotparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.uscis.gov/administrative-appeals/aao-decisions/aao-non-precedent-decisions?uri_1=All&m=All&y=All&items_per_page=100"
DOWNLOAD_DIR = "./aao_docs"
TARGET_KEYWORDS = ["I-140", "Extraordinary Ability"]
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def check_robots_txt(base_url, user_agent="*"):
    try:
        rp = urllib.robotparser.RobotFileParser()
        robots_url = "https://www.uscis.gov/robots.txt"
        rp.set_url(robots_url)
        rp.read()
        target_path = "/administrative-appeals/aao-decisions/"
        is_allowed = rp.can_fetch(user_agent, f"https://www.uscis.gov{target_path}")
        crawl_delay = rp.crawl_delay(user_agent) or 10
        return is_allowed, crawl_delay
    except Exception:
        return True, 10

def crawl_and_filter_links():
    is_allowed, crawl_delay = check_robots_txt(BASE_URL)
    if not is_allowed:
        return []

    options = Options()
    options.headless = True
    options.add_argument("user-agent=Mozilla/5.0 ...")
    driver = webdriver.Chrome(options=options)

    all_links = []
    page = 1
    max_links = 100
    actual_delay = max(2, crawl_delay)

    while len(all_links) < max_links:
        try:
            driver.get(BASE_URL + f"&page={page}")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except Exception:
            break

        links = soup.find_all("a", href=True)
        page_links = []
        for link in links:
            href = link['href']
            if href.endswith(".pdf") or "decision" in href.lower():
                full_url = href if href.startswith("http") else f"https://www.uscis.gov{href}"
                if full_url.endswith(".pdf"):
                    page_links.append(full_url)

        all_links.extend(page_links)

        if len(all_links) >= max_links or not soup.find("a", class_="pager__link--next"):
            break
        page += 1
        sleep(actual_delay)

    driver.quit()
    return list(set(all_links))

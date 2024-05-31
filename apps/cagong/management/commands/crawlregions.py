from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from django.db import transaction
from django.core.management.base import BaseCommand
from apps.cagong.models import Region

import logging

from datetime import datetime
import time
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

url = "https://www.juso.go.kr/info/RoadNameDataList.do?type=search&roadCd=&keyword=&city1=26&county1=&county1=&searchType=0&extend=true"


class Command(BaseCommand):
    help = "crawl regions"

    def extract(self):
        logger.info(f"#### Start to extract data")
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 헤드리스 모드로 실행
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        rows = list()

        city_elements = driver.find_element(By.CSS_SELECTOR, "select#city1")
        city_elements = Select(city_elements)
        for city_idx, city_element in enumerate(city_elements.options):
            city_code = city_element.get_attribute("value")
            if not city_code:
                continue
            city_name = city_element.text.strip()
            logger.info(f"start to crawl {city_name}")
            city_elements.select_by_index(city_idx)
            county_elements = driver.find_element(By.CSS_SELECTOR, "select#county1")
            county_elements = Select(county_elements)
            time.sleep(1)
            for county_idx, county_element in enumerate(county_elements.options):

                if city_name == "세종특별자치시":
                    county_code = "999"
                    county_name = ""
                else:
                    county_code = county_element.get_attribute("value")
                    if not county_code:
                        continue
                    county_name = county_element.text.strip()
                    county_elements.select_by_index(county_idx)
                town_elements = driver.find_element(By.CSS_SELECTOR, "select#town1")
                town_elements = Select(town_elements)
                time.sleep(1)
                for town_element in town_elements.options:
                    town_code = town_element.get_attribute("value")
                    if not town_code:
                        continue
                    town_name = town_element.text.strip()
                    row = {
                        "city_code": city_code,
                        "city_name": city_name,
                        "county_code": county_code,
                        "county_name": county_name,
                        "town_code": town_code,
                        "town_name": town_name,
                    }
                    rows.append(row)
        logger.info(f"#### Success to extract data")
        return rows

    def process(self, data):
        logger.info("#### Start to process data")
        df = pd.DataFrame(data)
        df["id"] = df["city_code"] + df["county_code"] + df["town_code"]
        logger.info("#### Success to process data")
        return df

    def load(self, df):
        logger.info(f"#### Start to load..")
        with transaction.atomic():
            for _, row in df.iterrows():
                obj, created = Region.objects.update_or_create(
                    id=row["id"],
                    defaults={
                        "city_code": row["city_code"],
                        "city_name": row["city_name"],
                        "county_code": row["county_code"],
                        "county_name": row["county_name"],
                        "town_code": row["town_code"],
                        "town_name": row["town_name"],
                        "updated_at": datetime.now(),
                    },
                )
                if created:
                    logger.info(f"Created: {obj}")
                else:
                    logger.info(f"Updated: {obj}")
        logger.info(f"#### Success to load data to region table")

    def handle(self, **options):
        data = self.extract()
        df = self.process(data)
        self.load(df)

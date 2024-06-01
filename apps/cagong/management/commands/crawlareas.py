from django.db import transaction
from django.core.management.base import BaseCommand
from apps.cagong.models import Area

import logging

from datetime import datetime
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

url = "https://www.juso.go.kr/info/RoadNameDataList.do?type=search&roadCd=&keyword=&city1=11&county1=&town1=&searchType=0&extend=true"


class Command(BaseCommand):
    help = "crawl areas"

    def extract(self):
        logger.info(f"#### Start to extract data")
        response = requests.get(url)
        if response.status_code == 200:
            html = response.text
        soup = BeautifulSoup(html, "html.parser")

        cities = soup.select("select#city1 option")
        city_dict = dict()
        for city in cities:
            value = city.attrs["value"]
            if value:
                title = city.attrs["title"]
                city_dict[value] = title

        rows = list()
        for city in city_dict:
            logger.info(f"start to crawl {city_dict[city]}")
            response = requests.get(
                f"https://www.juso.go.kr/getAreaCode.do?from=city&to=county&valFrom={city}&valTo=&rdIndex=undefined"
            )
            if response.status_code == 200:
                xml = response.text
                soup = BeautifulSoup(xml, features="lxml")
                values = [value.text for value in soup.find_all("value")]
                names = [name.text for name in soup.find_all("name")]
                county_dict = dict(zip(values, names))

                for county in county_dict:
                    time.sleep(0.3)
                    response = requests.get(
                        f"https://www.juso.go.kr/getAreaCode.do?from=county&to=town&valFrom={city}{county}&valTo=&rdIndex=undefined"
                    )
                    if response.status_code == 200:
                        xml = response.text
                        soup = BeautifulSoup(xml, features="lxml")
                        values = [value.text for value in soup.find_all("value")]
                        names = [name.text for name in soup.find_all("name")]
                        for value, name in zip(values, names):
                            city_code = city
                            city_name = city_dict[city]
                            county_code = county
                            county_name = county_dict[county]
                            town_code = value
                            town_name = name
                            row = {
                                "city_code": city_code,
                                "city_name": city_name,
                                "county_code": county_code,
                                "county_name": county_name,
                                "town_code": town_code,
                                "town_name": town_name,
                            }
                            rows.append(row)
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
                obj, created = Area.objects.update_or_create(
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
        logger.info(f"#### Success to load data to Area table")

    def handle(self, **options):
        data = self.extract()
        df = self.process(data)
        self.load(df)

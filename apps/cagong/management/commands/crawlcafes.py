from django.db import transaction
from django.core.management.base import BaseCommand
from apps.cagong.models import Region, Cafe
import requests
import logging

from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Command(BaseCommand):
    help = "crawl regions"

    def fetch(self, area, page, size):
        url = "https://im.diningcode.com/API/isearch/"
        data = {
            "query": "",
            "addr": area,
            "keyword": "카페",
            "order": "r_score",
            "distance": "",
            "rn_search_flag": "on",
            "search_type": "poi_search",
            "lat": "",
            "lng": "",
            "rect": "",
            "token": "",
            "mode": "",
            "dc_flag": "1",
            "page": str(page),
            "size": str(size),
        }
        headers = {
            "Cookie": "dcadid=WZRSJC1713788403",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            logger.info(f"status code {response.status_code}")

    def extract(self):
        logger.info(f"#### Start to extract data")
        rows = list()
        regions = Region.objects.values(
            "id",
            "city_name",
            "county_name",
            "town_name",
        )
        for region in regions:
            area_id = region.get("id")
            city_name = region.get("city_name")
            county_name = region.get("county_name")
            town_name = region.get("town_name")

            if county_name:
                area = f"{city_name} {county_name} {town_name}"
            else:
                area = f"{city_name} {town_name}"

            size = 20
            total_cnt = 100
            page_size = total_cnt // size + 1
            for page in range(1, page_size):
                print(f"{area}, page {page}")
                response = self.fetch(area, page, size)
                result_data = response["result_data"].get("poi_section")
                if result_data:
                    cafes = result_data["list"]
                    for cafe in cafes:
                        data = {
                            "crawl_id": cafe["v_rid"],
                            "name": cafe["nm"],
                            "addr": cafe["addr"],
                            "phone": cafe["phone"],
                            # "image": cafe["image"],
                            "lat": cafe["lat"],
                            "lng": cafe["lng"],
                            "area_id": area_id,
                        }
                        rows.append(data)
                else:
                    logger.info(f"There is no data in {area}")
                    break

        logger.info(f"#### Success to extract data")
        return rows

    def load(self, data):
        logger.info(f"#### Start to load..")
        with transaction.atomic():
            for row in data:
                _, created = Cafe.objects.update_or_create(
                    crawl_id=row["crawl_id"],
                    defaults={
                        "is_crawled": True,
                        "crawl_id": row["crawl_id"],
                        "name": row["name"],
                        "addr": row["addr"],
                        "phone": row["phone"],
                        "lat": row["lat"],
                        "lng": row["lng"],
                        "area_id": row["area_id"],
                        "updated_at": datetime.now(),
                    },
                )
                if created:
                    logger.info(f"Created: {row['crawl_id']}")
                else:
                    logger.info(f"Updated: {row['crawl_id']}")
        logger.info(f"#### Success to load data to cafe table")

    def handle(self, **options):
        data = self.extract()
        self.load(data)

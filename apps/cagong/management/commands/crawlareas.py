from django.db import transaction
from django.core.management.base import BaseCommand
from apps.cagong.models import Area

import logging

from datetime import datetime
from common.utils import get_dataframe_from_s3


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

bucket = "ca-devbucket"
file_key = "gisp-data-20240606/area.parquet"


class Command(BaseCommand):
    help = "crawl areas"

    def extract_process(self):
        logger.info("#### Start to extract, process data")
        df = get_dataframe_from_s3(bucket, file_key)
        df["id"] = df["city_code"] + df["county_code"] + df["town_code"]
        df["county_name"] = df["county_name"].fillna("")
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
        df = self.extract_process()
        self.load(df)

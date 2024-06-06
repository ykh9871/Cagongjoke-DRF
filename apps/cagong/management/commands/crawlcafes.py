from django.db import transaction
from django.core.management.base import BaseCommand
from apps.cagong.models import Cafe
from common.utils import get_dataframe_from_s3

import logging

from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Command(BaseCommand):
    help = "crawl cafes"

    def extract(self):
        logger.info(f"#### Start to extract data")
        bucket = "ca-devbucket"
        file_key = "gisp-data-20240606/cafe.parquet"
        df = get_dataframe_from_s3(bucket, file_key)
        logger.info(f"#### Success to extract data")
        return df

    def load(self, df):
        logger.info(f"#### Start to load..")
        with transaction.atomic():
            for row in df.to_dict(orient="records"):
                crawl_id = row["v_rid"]
                _, created = Cafe.objects.update_or_create(
                    crawl_id=crawl_id,
                    defaults={
                        "is_crawled": True,
                        "crawl_id": crawl_id,
                        "name": row["nm"],
                        "addr": row["addr"],
                        "phone": row["phone"],
                        "lat": row["lat"],
                        "lng": row["lng"],
                        "area_id": row["area_id"],
                        "updated_at": datetime.now(),
                    },
                )
                if created:
                    logger.info(f"Created: {crawl_id}")
                else:
                    logger.info(f"Updated: {crawl_id}")
        logger.info(f"#### Success to load data to cafe table")

    def handle(self, **options):
        data = self.extract()
        self.load(data)

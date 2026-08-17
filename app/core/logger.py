import logging

logging.basicConfig(
    filename="app/logs/business_api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

import logging
import os

os.makedirs("logs",exist_ok=True)
#logger creation
ml_logger = logging.getLogger(__name__)
ml_logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/ml_logging.log",encoding = "utf-8")
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler.setFormatter(formatter)
ml_logger.addHandler(handler)

import logging
import os

os.makedirs("logs",exist_ok=True)
#logger creation
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("logs/logging.log",encoding = "utf-8")
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

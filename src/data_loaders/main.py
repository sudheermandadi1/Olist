from src.utils.logger import logger
from src.data_loaders.Customer_loader import load_customer
from src.data_loaders.Order_item_loader import load_order_items
from src.data_loaders.Orders_loader import load_orders
from src.data_loaders.seller_loader import load_sellers
from src.data_loaders.Product_loader import load_products


def main():
    logger.info("=============================")
    logger.info("OLIST DATA PIPELINE STARTED")
    logger.info("=============================")

    try:
        load_customer("data/olist_customers_dataset.csv")

        load_orders("data/olist_orders_dataset.csv")

        load_products("data/olist_products_dataset.csv")

        load_sellers("data/olist_sellers_dataset.csv")


        load_order_items("data/olist_order_items_dataset.csv")


        logger.info("======================================")
        logger.info("OLIST DATA PIPELINE COMPLETED")
        logger.info("=======================================")
        print("sucessfully executed...")

    except Exception:
        logger.exception("OLIST DATA PIPELINE FAILED")

        raise




if __name__ ==  "__main__" :
    main()

from .models import Campaign, CampaignType
from django.core.cache import cache
from __common__ import CSV, RedisC


# Create a user segment
## Create a product segment

def get_prices(course_ids: list, user_id=None):
    ## search MP(L)

    return [{"amount": 123} for i in course_ids]

def ingest_campaign_prices(campaign):
    ##
    pass

# Class BaseCampaign

# Class EarlyBird()
#     def get_user_segment()
#     def get_products()
#     def get_price(user_id, product_id)
#     def pause_campaign()
#     def restart_campaign()
#     def modify_user_segment()
#     def modify_product()
#     def is_active()

# Class FlashSale()
#     def get_user_segment()
#     def get_products()
#     def get_price(user_id, product_id)
#     def pause_campaign()
#     def restart_campaign()
#     def modify_user_segment()
#     def modify_product()
#     def is_active()



# Loookup : MasterPriceList (all campaigns)
#     - given a product_id and user_id, return price (base query)
#     - given a list of product_ids and user_id, return price (faster search)
#     - given a list of user_ids and a product, return price (for marketing campaigns)



# INPUT 1 : flash_sale_1, COURSES: all_art_courses, users: [1,22,34,45,66,7 ... 78341], price = 2344
# INPUT 2 : early_bird, COURSES : [1,2,3], users: all
# INPUT 3 : 




def get_product_price(user_id, product_id):
    campaign_price = RedisC().get(f"PRICE:{product_id}:{user_id}")
    if not campaign_price:
        return 100

    return campaign_price

def get_product_price_bulk(user_id, product_ids):
    pass

def update_price(product_id):
    pass

def create_campaign():
    pass

## Segments to ids (product & user) mapping
def ingest_user_segment(segment_name: str, user_ids: list):
    RedisC().set(f"USER_{segment_name}", *set(user_ids))

def is_user_in_segment(segment_name: str, user_id: int):
    return RedisC().sismember(f"USER_{segment_name}", user) == True

def ingest_product_segment(segment_name: str, user_ids: list):
    RedisC().set(f"PRODUCT_{segment_name}", *set(user_ids))

def is_product_in_segment(segment_name: str, product_id: int):
    return RedisC().sismember(f"USER_{segment_name}", user) == True


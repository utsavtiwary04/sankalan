from .models import Campaign, PriceProfile
from django.core.cache import cache
from __common__ import redis_client

Campaign
- name
- description
- created_by
- type
- start/end

UserSegment
- name
- created_by
- description
- user_count

ProductSegment
- name
- type (product_id, category_id)
- entity_id


Class BaseCampaign

Class EarlyBird()
	def get_user_segment()
	def get_products()
	def get_price(user_id, product_id)
	def pause_campaign()
	def restart_campaign()
	def modify_user_segment()
	def modify_product()
	def is_active()

Class FlashSale()
	def get_user_segment()
	def get_products()
	def get_price(user_id, product_id)
	def pause_campaign()
	def restart_campaign()
	def modify_user_segment()
	def modify_product()
	def is_active()



Loookup : MasterPriceList (all campaigns)
	- given a product_id and user_id, return price (base query)
	- given a list of product_ids and user_id, return price (faster search)
	- given a list of user_ids and a product, return price (for marketing campaigns)

Let us do some calculations
3000 products, 1mn users
we run 10 sales every month
each user segment has on an average 10k users
each product segment has 25 products

Pricing matrix :
Monthly data volume (worst case) =  10 sales x 10k users x 25 products = 2.5mn entries
Yearly data volume (worst case) = 30mn entries


INPUT 1 : flash_sale_1, COURSES: all_art_courses, users: [1,22,34,45,66,7 ... 78341], price = 2344
INPUT 2 : early_bird, COURSES : [1,2,3], users: all
INPUT 3 : 




def get_product_price(user_id, product_id):
	pass

def get_product_price_bulk(user_id, product_ids):
	pass

def update_price(product_id, {}):
	pass


## Segments to ids (product & user) mapping
def ingest_user_segment(segment_name: str, user_ids: list):
	redis_client().set(f"USER_{segment_name}", *set(user_ids))

def is_user_in_segment(segment_name: str, user_id: int):
	return redis_client().sismember(f"USER_{segment_name}", user) == True

def ingest_product_segment(segment_name: str, user_ids: list):
	redis_client().set(f"PRODUCT_{segment_name}", *set(user_ids))

def is_product_in_segment(segment_name: str, product_id: int):
	return redis_client().sismember(f"USER_{segment_name}", user) == True


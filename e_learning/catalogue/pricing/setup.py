## Pre requisites, catalogue/setup.py should have run successfully
from catalogue.pricing.models import Campaign, ProductSegment, UserSegment, CampaignType, CampaignStatus
from catalogue.pricing.service import ingest_campaign_prices
from __common__.redis_client import RedisC
from __common__ import CSV, service_hub as Hub
from datetime import datetime


users_file    = "https://drive.google.com/uc?id=1L9H1QAgMQSPnJ2uT__C-1_JpvZmvFjv2"
products_file = "https://drive.google.com/uc?id=1OnEYBu4YAxRBS_6lMgCf984QChZG3l8c"
users         = CSV(users_file)
products      = CSV(products_file)


user_segment_json = {
	"name"        : "flash_sale_sept23_25k_active",
	"description" : "Alpha team led marketing campaign : price drop for 25k users for 2 days on 2 courses",
	"created_by"  : Hub.get_user(1),
	"user_count"  : len(users.data()),
	"file_url"    : users_file,
	"segment_key" : UserSegment.generate_segment_key("flash_sale_sept23_25k_active")
}
product_segment_json = {
	"name"          : "flash_sale_sept23_2courses_active",
	"description"   : "Alpha team led marketing campaign : price drop for 25k users for 2 day on 2 courses",
	"created_by"    : Hub.get_user(1),
	"product_count" : len(products.data()),
	"file_url"      : products_file,
	"segment_key"   : ProductSegment.generate_segment_key("flash_sale_sept23_25k_active"),
}
campaign_json = {
	"name"        : "flash_sale_sept23_25k_active",
	"description" : "Alpha team led marketing campaign : price drop for 25k users for 2 days on 2 courses",
	"created_by"  : Hub.get_user(1),
	"type"        : CampaignType.DIRECT
}

campaign = Campaign.objects.create(**campaign_json)

user_segment           = UserSegment(**user_segment_json)
user_segment._user_ids = [int(u["user_id"]) for u in users.data()]
user_segment.save()

product_segment              = ProductSegment(**product_segment_json)
product_segment._product_ids = [int(p["product_id"]) for p in products.data()]
product_segment.save()


# ingest_campaign_prices(campaign)




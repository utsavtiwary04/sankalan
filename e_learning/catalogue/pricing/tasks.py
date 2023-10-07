from __common__.redis_client import RedisC
from celery import shared_task


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def prepare_master_price(campaign_id):
    from .models import Campaign, ProductSegment, UserSegment, CampaignType

    campaign = Campaign.active_campaign(campaign_id)
    if not campaign:
        raise Exception(f"Invalid campaign ID or not found :: {campaign_id}")

    products = campaign.product_segment.product_prices_from_source() ## [{ "product_id": 1, "currency": "INR", "price": 4599 }]
    users    = campaign.user_segment.user_ids

    if campaign.type == CampaignType.COUPON:
        ## Get coupon and calculate price of each good
        pass

    if campaign.type == CampaignType.DIRECT:
        ## validate all products (should be done here as ingestion might happen later than segment creation)

        for product in products:
            for user_id in users:
                try:
                    RedisC().set(f"""PRICE:{product["product_id"]}:{user_id}""", product["amount"])
                except Exception as e:
                    print(f"""Failed to ingest price for product {product["product_id"]} and user {user_id} :: {e}""")

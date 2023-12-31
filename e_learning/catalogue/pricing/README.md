## 🏷️ Catalogue => Pricing


### Prologue

Pricing products is both complex fascinating in online commerce - particularly at scale. Almost all of us are familiar with "flash sales", "exclusive coupons", "early bird deals", "bundle offers" and so on. Behind the curtains, each e-commerce platform has a incredibly complex (also operationally heavy) mechanism for setting just the right price to make sure the bottom-line targets are met.

We will explore some of the fundamental techniques and build the underlying system which is reasonably felxible and scalable and most importantly - fully functional.

### What does it do ?

On the elearning platform that we have built for teachers, we will extend the following capabilities for teachers to increase sales of the courses. 

- 🦅 **Early bird deals**
- ⚡️ **Flash sales**
- ⏰ **Latecomer deal**
- 💫 **Special pricing on all art courses - no coupon needed !!**
- "add your request here ?"


We can assume a scale of 1million registered users on the platform and 3000 courses (unique SKUs) on offer by 300 teachers. Some of our teachers constantly offer early bird deals and run flash sales. Additionally, we offer discounts on certain categories and courses from time to time.

To visualize a complex situation, consider the following diagram 👇🏻👇🏻
<img src="https://lh3.googleusercontent.com/d/1FjUn_raztarQ-svOsof5iehg7WIH1hsu" width="800" height="400" alt="simultaneous_sale_on_user_product_segments"/>

------------------------------------------------------------------------------------------
</br>


##### Mechanisms for offering discount -
- Coupons (link here)
- Direct discount without coupons (login and get discounted rate directly upon checkout)
- Promotional credits/coins in wallet

Both have their specific user-experience and benefits around tracking so we cannot really put our finger and say -"well, we will only go with coupons because .."

Direct discounts are faster while coupons give you that "rewarding" feeling of having secured a sweet deal for yourself. We can add more arguments to each option but that's a debate for another day.

#### Workflow
The whole workflow can be divided into the following steps :
- Identifying the products to be given at a differential price (product list)
- Segmenting user(s) who have to offered this product at this special price (user segment)
- Configuring the details of the sale campaign or offer (start, end, value and more)
- Allowing manual overrides to campaigns at any stage of the campaign

Often your communication channel would be an external tool like Mailchimp, Gupshup etc. You will need to hook up to those APIs accordingly (which we can tackle in a separate post)

Let us do some calculations
3000 products, 1mn users
we run 10 sales every month
each user segment has on an average 10k users
each product segment has 25 products

Pricing matrix :
Monthly data volume (worst case) =  10 sales x 10k users x 25 products = 2.5mn entries
Yearly data volume (worst case) = 30mn entries


### Diagram


### Code Explanation


### Key Learnings
- Implementing pricing strategies
- Indexing prices of products
- Segmenting users and products and creating a pricing matrix for fast lookup


### Useful links

1. [Pricing strategies in marletplaces - some concepts](https://www.sellerapp.com/blog/top-essential-ecommerce-pricing-strategies/)

2. [Storing customer segments - Glovo](https://medium.com/glovo-engineering/customer-segmentation-at-glovo-8b46a787ac5e)

3. [Lookup tables](https://medium.com/capital-one-tech/blazing-fast-data-lookup-in-a-microservices-world-dd3ae548ca45)

### Further Learning

1. [Postgres Arrays](https://news.ycombinator.com/item?id=4415754)
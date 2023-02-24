# Rugstudio Crawler
Rugstudio is one of the largest retailers of rugs topic. In this repo, you can access scripts that crawl it.

## What's the purpose
This crawler scrapes the PLP and PDP pages and gets the title, description,  feature, image URL (and download file ability), and prices table.
</br>PLP: Product List Page
</br>PDP: Product Detail Page

## Structure
You can crawl all the brands or some of them in this crawler script. You can add or edit brands you want to crawl at the
"brand" table in the "database.db" file. For example, some brands were added to the "brand" table.

## How to work it:

### First time:
The first time, you should get PDP's URL. You can choose two options:
</br>1. Get all product URLs.
</br>2. Get product URLs of brands you need.
</br>After this step, you must crawl the details of the product page.

### Check prices:
After the crawl details of the product, you can check the product prices at any time, and you should just run the "Check price" option. You can set a percentage of a price change that sending an email.



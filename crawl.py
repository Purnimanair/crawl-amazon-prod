import requests
import re
import json
import csv

def fetch_html(url):
    response = requests.get(url)
    return response.text

def extract_data(html, url):
    # Define regex patterns to extract data points
    title_pattern = re.compile(r'<h1.*?>(.*?)<\/h1>')
    brand_pattern = re.compile(r'"brand":"(.*?)"')
    deal_price_pattern = re.compile(r'"dealPrice":"([0-9.]+)"')
    mrp_pattern = re.compile(r'"mrp":"([0-9.]+)"')
    thumbnail_pattern = re.compile(r'"thumbnail":"(.*?)"')
    reviews_pattern = re.compile(r'"reviewCount":(\d+)')
    rating_pattern = re.compile(r'"ratingValue":([0-9.]+)')
    product_details_pattern = re.compile(r'<div class="product-details">(.*?)<\/div>', re.DOTALL)
    meta_breadcrumbs_pattern = re.compile(r'<div class="breadcrumbs">(.*?)<\/div>', re.DOTALL)

    title = title_pattern.search(html).group(1) if title_pattern.search(html) else 'N/A'
    brand = brand_pattern.search(html).group(1) if brand_pattern.search(html) else 'N/A'
    deal_price = float(deal_price_pattern.search(html).group(1)) if deal_price_pattern.search(html) else 0.0
    mrp = float(mrp_pattern.search(html).group(1)) if mrp_pattern.search(html) else 0.0
    thumbnail_url = thumbnail_pattern.search(html).group(1) if thumbnail_pattern.search(html) else 'N/A'
    reviews = int(reviews_pattern.search(html).group(1)) if reviews_pattern.search(html) else 0
    rating = float(rating_pattern.search(html).group(1)) if rating_pattern.search(html) else 0.0
    product_details = product_details_pattern.search(html).group(1).strip() if product_details_pattern.search(html) else 'N/A'
    meta_breadcrumbs = meta_breadcrumbs_pattern.search(html).group(1).strip() if meta_breadcrumbs_pattern.search(html) else 'N/A'

    return {
        'title': title,
        'brand': brand,
        'deal_price': deal_price,
        'mrp': mrp,
        'url': url,
        'thumbnail_url': thumbnail_url,
        'reviews': reviews,
        'rating': rating,
        'product_details': product_details,
        'meta_breadcrumbs': meta_breadcrumbs
    }

def write_to_json(data_list, filename='products.jsonl'):
    with open(filename, 'w') as jsonfile:
        for data in data_list:
            jsonfile.write(json.dumps(data) + '\n')  # Write each product as one line of JSON


def jsonl_to_csv(jsonl_file, csv_file):
    with open(jsonl_file, 'r') as f, open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['title', 'brand', 'deal_price', 'mrp', 'url', 'thumbnail_url', 'reviews', 'rating', 'product_details', 'meta_breadcrumbs']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for line in f:
            product_data = json.loads(line)         
            writer.writerow(product_data)

def crawl_and_convert_to_csv(product_urls, jsonl_file='products.jsonl', csv_file='products_output.csv'):
    all_data = []
    
    for url in product_urls:
        html = fetch_html(url)
        data = extract_data(html, url)
        all_data.append(data)
    
    # Write extracted data to a JSONL file
    write_to_json(all_data, jsonl_file)
    
    # Convert the JSONL file to CSV
    jsonl_to_csv(jsonl_file, csv_file)

product_urls = [
    "https://www.amazon.in/gp/product/B07WDJZY5Q/ref=s9_bw_cg_Budget_4b1_w",
    "https://www.amazon.in/iQOO-Storage-Snapdragon%C2%AE-Platform-Flagship/dp/B07WGMXVFK",
    "https://www.amazon.in/dp/B0DGJ3THPR",
    "https://www.amazon.in/dp/B0CHX3TW6X"
]
crawl_and_convert_to_csv(product_urls)

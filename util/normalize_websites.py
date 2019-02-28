def normalize_website(website_url):
    website_url = website_url.lower()
    return website_url.replace('http://', '').replace('https://', '').replace('www.', '').strip('/')

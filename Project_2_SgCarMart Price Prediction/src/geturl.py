import requests
from bs4 import BeautifulSoup

# URL to Scrape from
url = 'https://www.sgcarmart.com/used_cars/listing.php?RPG=20&VEH=1&AVL=2&ORD='

# Base url, or you can think of this as the individual car listing prefix
base_url = 'https://www.sgcarmart.com/used_cars/'

# Make a request to the website and get the object
content = requests.get(url)

# Parse the HTML text
soup = BeautifulSoup(content.text,'html.parser')

# Find every single URL in the webpage , refer to this post: https://stackoverflow.com/questions/46490626/getting-all-links-from-a-page-beautiful-soup
# This returns a list of every tag that contains a link in the webpage
links = soup.find_all('a')

# Create empty list
listing_urls = []


for link in links:
    # Get the link
    suffix = link.get('href')

    # Check if 'ID=' and 'DL=' exist in the string
    if ('ID=' in suffix) and ('DL=' in suffix):

        # Concatenate the two strings if they do
        listing_url = base_url + suffix
        # Append result to the list
        listing_urls.append(listing_url)


# Print out each car listing url
for listing_url in listing_urls:
    print(listing_url)
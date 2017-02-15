from lxml import html
import requests
import csv
import user_funcs
import numpy as np

# Global Variables

sqmresearch_generic = 'http://www.sqmresearch.com.au/sold-properties.php?postcode='
page_numbers = ['','&p=2','&p=3','&p=4']
prices = []
street_address = []
postcode = []
date = []
bedrooms = []
bathrooms = []
cars = []

"""
# Create Local csv file of Melbourne Postcodes
melbourne_postcodes = user_funcs.create_melb_postcodes()
melbourne_postcodes_csv = '/Users/weiner103/Documents/Real Estate Project/MelbPostCodes.csv'
user_funcs.write_array_csv(melbourne_postcodes_csv,melbourne_postcodes)
"""

# Read in csv file of Melbourne Postcodes into variable
local_melb_postcodes = user_funcs.read_array_csv('/Users/weiner103/Documents/Real Estate Project/MelbPostCodes.csv')

# Scrape website in increments of 1/8's
total_postcodes = len(local_melb_postcodes)
one_eigth_total = total_postcodes/8
final_postcode = 0
number_of_postcodes_scraped = 0
number_of_eights_scraped = 1

# number_of_eights_scraped * one_eigth_total+1,(number_of_eights_scraped+1) * one_eigth_total
for i in range(number_of_eights_scraped * one_eigth_total+1,(number_of_eights_scraped * one_eigth_total+1)+1):
	for j in range(0,len(page_numbers)-1):
		website_request = requests.get(sqmresearch_generic + str(local_melb_postcodes[i]) + page_numbers[j])
		website_tree = html.fromstring(website_request.content)
		no_of_houses_before = len(prices)
		prices.extend(website_tree.xpath('//div[@class="spr_rightcol"]/p/b/text()'))
		street_address.extend(website_tree.xpath('//div[@class="spr_rightcol"]/h3/a/text()'))
		date.extend(website_tree.xpath('//div[@class="spr_rightcol"]/p/text()'))
		for k in range(0,len(prices)-no_of_houses_before):
			postcode.append(str(local_melb_postcodes[i]))
		if website_tree.xpath('//div[@class="spr_beds"]/text()') is not None:
			bedrooms.extend(website_tree.xpath('//div[@class="spr_beds"]/text()'))
		else:
			bedrooms.extend(0)
		if website_tree.xpath('//div[@class="spr_bath"]/text()') is not '':
			bathrooms.extend(website_tree.xpath('//div[@class="spr_bath"]/text()'))
#print website_tree.xpath('//div[@class="spr_bath"]/text()')
		else:
			bathrooms.extend(0)
			print 'found it'
		if website_tree.xpath('//div[@class="spr_cars"]/text()') is not None:
			cars.extend(website_tree.xpath('//div[@class="spr_cars"]/text()'))
		else:
			cars.extend(0)
final_postcode = i

print final_postcode
csv_file = open('/Users/weiner103/Documents/Real Estate Project/Data2.csv', 'wt')
try:
    writer = csv.writer(csv_file)
    writer.writerow( ('Prices', 'Location','Postcode', 'Date', 'Bedrooms', 'Bathrooms', 'Carports'))
    for i in range(1,len(prices)):
        writer.writerow((prices[i-1], street_address[i-1],postcode[i-1],date[2*i+1],bedrooms[i-1],bathrooms[i-1],cars[i-1]))
finally:
    csv_file.close()

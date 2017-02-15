import csv
import requests
from lxml import html


def create_melb_postcodes():
	melb_postcodes_url = 'http://www.postcodes-australia.com/state-postcodes/vic'
	try:
		melbourne_postcodes_website = requests.get(melb_postcodes_url, timeout=10)
		melbournes_postcodes_tree = html.fromstring(melbourne_postcodes_website.content)
		melbourne_postcodes = melbournes_postcodes_tree.xpath('//ul[@class="pclist"]/li/a/text()')
		return melbourne_postcodes
	except:
		print('Timeout error has occured')

def write_array_csv(file_name,data):
	with open(file_name, 'wb') as f:
		try:
			writer = csv.writer(f)
			for i in range(len(data)):
				writer.writerow([data[i]])
		finally:
			f.close()

def read_array_csv(file_name):
	data_read = []
	with open(file_name,'rb') as f:
		try:
			reader = csv.reader(f)
			for row in reader:
				data_read.extend(row)
			return data_read
		finally:
			f.close()







			  
			  
			  
			  
			  

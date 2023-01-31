from bs4 import BeautifulSoup
import requests
import csv

# name has minimum of 3 characters
name = "ann"

def get_soup(name, page_number):
  url = f"https://registers.consumer.vic.gov.au/RhoSearch/SearchResult?PageNumber={page_number}&Name={name}"
  req = requests.get(url)
  soup = BeautifulSoup(req.text, "html.parser")
  
  return soup

soup = get_soup(name, 1)
table_soup = soup.select_one('div.search-results-area > div.row > table')
if table_soup is None:
  print("No results found OR table 'div.search-results-area > div.row > table' not exists")

thead_row = table_soup.select_one('thead > tr')
headers = [th.getText().strip() for th in thead_row.select('.tableHeaderFont')]

page_numbers = [int(page.getText()) for page in soup.select('div.page-numbers > ol > li')]
max_page = 1
if len(page_numbers) > 0:
  max_page = max(page_numbers)

row_data = []
for p in range(1, max_page + 1):
  if p > 1:
    soup = get_soup(name, p)

  table_soup = soup.select_one('div.search-results-area > div.row > table')
  tbody_rows = table_soup.select('tbody > tr')

  for row in tbody_rows:
    row_data.append([td.getText().strip() for td in row.select('td')])

with open(f'output_{name}.csv', 'w', encoding='utf-8', newline='') as f:
  writer = csv.writer(f)
  writer.writerow(headers)
  writer.writerows(row_data)
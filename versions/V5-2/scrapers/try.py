import csv

records =[]
name = "Gold"

with open(f'../files/{name}.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Month', 'Price', 'Change'])
    writer.writerows(records)


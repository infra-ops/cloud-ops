import csv

f_r = open("test.csv", 'r')
f_w = open("test_new.txt", 'w')

dr = csv.DictReader(f_r)
field_names = dr.fieldnames

print field_names

new_field_names  = ['price', 'title', 'authors', 'binding', 'pages',  'book_id',  'isbn', 'image_url']

dw = csv.DictWriter(f_w, new_field_names, delimiter=",", quotechar='|')
dw.writeheader()

for line in dr:
    dw.writerow(line)

f_w.close()
f_r.close()
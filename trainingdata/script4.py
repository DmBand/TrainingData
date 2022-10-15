from bs4 import BeautifulSoup

file1 = open('annotations.xml')
file2 = open('annotations-2.xml')
file3 = open('annotations-3.xml')
new_file = open('new.xml', 'w')

soup = BeautifulSoup(file1, parser='xml', features='lxml')
image_tag = soup.find_all('image')
image_ids = [img['id'] for img in image_tag]

position = -1
for img in image_tag:
    img['id'] = image_ids[position]
    position -= 1
    current_name = img['name'].split('/')[-1]
    new_name = current_name.split('.')[0] + '.png'
    img['name'] = new_name

new_file.write(soup.prettify())
new_file.close()

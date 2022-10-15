from bs4 import BeautifulSoup

file1 = open('annotations.xml')
file2 = open('annotations-2.xml')
file3 = open('annotations-3.xml')

soup = BeautifulSoup(file2, parser='xml', features='lxml')

image_tag = soup.find_all('image')
marked_up_images = [img for img in image_tag if img.find()]

data = {}
for tag in marked_up_images:
    for figure in tag.find_all():
        name = figure.name
        if name in data:
            data[name] += 1
        else:
            data[name] = 1

for item in data:
    print(f'{item}: {data[item]} шт')

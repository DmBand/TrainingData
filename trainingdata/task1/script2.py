from bs4 import BeautifulSoup

file1 = open('annotations.xml')
file2 = open('annotations-2.xml')
file3 = open('annotations-3.xml')

soup = BeautifulSoup(file2, parser='xml', features='lxml')

image_tag = soup.find_all('image')
marked_up_images = [img for img in image_tag if img.find()]
data = {}
for tag in marked_up_images:
    figures = tag.find_all()
    for f in figures:
        label = f['label']
        if label in data:
            data[label] += 1
        else:
            data[label] = 1

for item in data:
    print(f'{item}: {data[item]} фигур')

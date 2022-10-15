from bs4 import BeautifulSoup

file1 = open('annotations.xml')
file2 = open('annotations-2.xml')
file3 = open('annotations-3.xml')

soup = BeautifulSoup(file3, parser='xml', features='lxml')

image_tag = soup.find_all('image')
# 1. Всего изображений
number_of_images = len(image_tag)
# 2. Всего размечено
marked_up_images = len([img for img in image_tag if img.find()])
# 3. Всего не размечено
not_marked_up_images = number_of_images - marked_up_images
# 5. Количество фигур
number_of_figures = sum(len(img.find_all()) for img in image_tag)
# 6. Общая статистика


# a = image_tag[-4]
# b = image_tag[0]
print(number_of_images)
print(marked_up_images)
print(not_marked_up_images)
print(number_of_figures)

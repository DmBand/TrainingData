from bs4 import BeautifulSoup

file1 = open('annotations.xml')
file2 = open('annotations-2.xml')
file3 = open('annotations-3.xml')

soup = BeautifulSoup(file1, parser='xml', features='lxml')

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
initial_width = int(image_tag[0]['width'])
initial_height = int(image_tag[0]['height'])
statistics = {
    'biggest': {
        'width': initial_width,
        'height': initial_height,
        'count': 1
    },
    'smallest': {
        'width': initial_width,
        'height': initial_height,
        'count': 1
    }
}
biggest_area = smallest_area = initial_width * initial_height
for tag in image_tag[1:]:
    tag_width = int(tag['width'])
    tag_height = int(tag['height'])
    tag_area = tag_width * tag_height

    if tag_area > biggest_area:
        biggest_area = tag_area
        statistics['biggest']['width'] = tag_width
        statistics['biggest']['height'] = tag_height
        statistics['biggest']['count'] = 1
    elif tag_area == biggest_area:
        statistics['biggest']['count'] += 1
    if tag_area < smallest_area:
        smallest_area = tag_area
        statistics['smallest']['width'] = tag_width
        statistics['smallest']['height'] = tag_height
        statistics['smallest']['count'] = 1
    elif tag_area == smallest_area:
        statistics['smallest']['count'] += 1

# print(number_of_images)
# print(marked_up_images)
# print(not_marked_up_images)
# print(number_of_figures)
# print('Самое большое изображение:\n'
#       f'ширина: {statistics["biggest"]["width"]}, '
#       f'высота: {statistics["biggest"]["height"]}, '
#       f'количество: {statistics["biggest"]["count"]}\n'
#       'Самое маленькое изображение:\n'
#       f'ширина: {statistics["smallest"]["width"]}, '
#       f'высота: {statistics["smallest"]["height"]}, '
#       f'количество: {statistics["smallest"]["count"]}')

import os

from bs4 import BeautifulSoup
from PIL import Image, ImageDraw


def get_coordinates(figures):
    all_coordinates = []
    for figure in figures:
        one = []
        if figure['label'] == 'Ignore':
            continue
        else:
            coord = figure['points'].split(';')
            for value in coord:
                tup = tuple(map(lambda num: float(num), value.split(',')))
                one.append(tup)
            all_coordinates.append(one)
    return all_coordinates


def get_image_tag(name: str, bs: BeautifulSoup):
    for image_tag in bs.find_all('image'):
        if name in image_tag['name']:
            return image_tag


def draw_polygon(points: list,
                 draw_rgb: ImageDraw,
                 draw_rgba: ImageDraw,
                 color: tuple = (162, 41, 232)) -> tuple:
    for c in points:
        draw_rgb.polygon(c, fill=color)
        draw_rgba.polygon(c, fill=color)
    return draw_rgb, draw_rgba


with open('masks.xml') as masks:
    images = os.listdir('images')
    soup = BeautifulSoup(masks, parser='xml', features='lxml')
    for image_name in images:
        tag = get_image_tag(image_name, soup)
        original_img = Image.open(f'images/{image_name}').copy()
        pol_for_one_img = tag.find_all()
        coordinates = get_coordinates(pol_for_one_img)
        mask_im_rgba = Image.new('RGBA', original_img.size)
        mask_im_rgb = Image.new('RGB', original_img.size, 0)
        image_rgba = ImageDraw.Draw(mask_im_rgba)
        image_rgb = ImageDraw.Draw(mask_im_rgb)
        masks = draw_polygon(coordinates, image_rgb, image_rgba)
        mask_im_rgb.save(f'new_images/mask_{image_name}.jpg')
        original_img.paste(mask_im_rgba, (0, 0), mask_im_rgba)
        original_img.save(f'new_images/with_mask_{image_name}.png')
        original_img.close()

# file1 = open('masks.xml')
# # teg = get_image_tag(file1, '0810f8ff-0fe1-4b1c-b4cc-73b6d96a8c37.jpg')
# # print(teg['name'])
#
# soup = BeautifulSoup(file1, parser='xml', features='lxml')
#
# img = soup.find('image')
#
# im = Image.open('0810f8ff-0fe1-4b1c-b4cc-73b6d96a8c37.jpg')
#
# pol_for_one_img = img.find_all()
# coordinates = []
# for img in pol_for_one_img:
#     one = []
#     coord = img['points'].split(';')
#     for value in coord:
#         tup = tuple(map(lambda num: float(num), value.split(',')))
#         one.append(tup)
#     coordinates.append(one)
# # print(coordinates)
#
# mask_im_rgba = Image.new('RGBA', im.size)
# mask_im_rgb = Image.new('RGB', im.size, 0)
# draw = ImageDraw.Draw(mask_im_rgba)
# draw2 = ImageDraw.Draw(mask_im_rgb)
# for c in coordinates:
#     draw.polygon(c, fill=(162, 41, 232))
#     draw2.polygon(c, fill=(162, 41, 232))
# mask_im_rgb.save('mask.jpg')
# im_ = im.copy().convert('RGBA')
# im_.paste(mask_im_rgba, (0, 0), mask_im_rgba)
# im_.save('dima.png')


# #
# text = [(421.50,731.97), (419.35,730.54), (417.06,729.39), (414.77,728.39), (412.47,727.67),
#         (410.18,726.81), (408.03,726.09), (405.74,725.38), (403.45,724.95), (402.87,727.10),
#         (404.30,729.53), (406.17,730.68), (409.75,734.12), (411.61,735.70), (413.33,737.41),
#         (414.34,739.56), (415.48,741.43), (416.63,743.29), (418.35,744.87), (420.07,746.59),
#         (421.79,748.16), (423.51,749.74), (425.80,750.03), (428.09,750.17), (430.24,749.45),
#         (431.82,747.30), (432.25,745.15), (432.39,743.00), (432.10,740.85), (430.82,738.99),
#         (428.81,737.13), (426.95,735.70), (425.08,734.41), (423.51,732.83)]
# text2 = [(951.29,1010.31), (950.70,1005.85), (950.70,1001.10), (953.67,997.53), (955.75,993.37),
#          (959.02,988.91), (962.29,984.16), (965.86,980.59), (969.12,976.14), (971.50,971.08),
#          (973.28,966.92), (975.07,962.76), (978.34,959.20), (980.12,963.66), (981.60,968.11),
#          (983.39,972.27), (984.87,977.03), (986.36,981.78), (986.95,986.24), (983.98,990.10),
#          (980.12,993.37), (975.96,995.75), (971.80,998.42), (968.23,1001.39), (964.37,1003.77),
#          (960.80,1006.74), (956.64,1008.52)]
# pprint(text)
# draw.polygon(text2, fill=255)
# draw.polygon(text, fill=255)
# mask_im.save('new_images2.jpg')

# pol = img.find_all()[0]
# coord = pol['points'].split(';')
# coord2 = list(map(lambda i: tuple(i.split(',')), coord))
# coord3 = [(float(i[0]), float(i[1])) for i in coord2]
# print(coord3)
# # print(coord3)
# mask_im = Image.new_images2('L', im.size, 112)
# draw = ImageDraw.Draw(mask_im)
# draw.polygon(coord3, fill=255)
# mask_im.save('new_images2.jpg')
# '162.0, 41.0, 232.0'

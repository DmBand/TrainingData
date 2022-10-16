import os

from bs4 import BeautifulSoup, Tag
from PIL import Image, ImageDraw


def get_image_tag(name: str, bs: BeautifulSoup) -> Tag:
    """
    Находит и возвращает соответствующий тег изображения
    с именем "name".
    :param name: Параметр name у тега изображения.
    :param bs: Экземпляр класса BeautifulSoup
    """

    for image_tag in bs.find_all('image'):
        if name in image_tag['name']:
            return image_tag


def get_coordinates(figures: list) -> list:
    """
    Возвращает полный список координат
    для одного изображения.
    :param figures: Список необработанных координат.
    """

    all_coordinates = []
    for figure in figures:
        one_figure_coordinates = []
        if figure['label'] == 'Ignore':
            continue
        else:
            coord = figure['points'].split(';')
            for value in coord:
                coord = tuple(map(float, value.split(',')))
                one_figure_coordinates.append(coord)
            all_coordinates.append(one_figure_coordinates)

    return all_coordinates


def draw_polygon(points: list,
                 draw_rgb: ImageDraw,
                 draw_rgba: ImageDraw,
                 color: tuple = (162, 41, 232)) -> None:
    """
    Рисует два многоугольника по заданным координатам.
    :param points: Список координат.
    :param draw_rgb: Многоугольник на черном фоне.
    :param draw_rgba: Многоугольник на прозрачном фоне.
    :param color: Цвет заполнения маски
    """

    for c in points:
        draw_rgb.polygon(c, fill=color)
        draw_rgba.polygon(c, fill=color)


def main(original_images_path: str,
         new_images_path: str,
         mask_path: str) -> None:
    """
    :param original_images_path: Путь к папке, в которой
    хранятся необработанные изображения.
    :param new_images_path: Путь к папке, в которой
    хранятся обработанные изображения и маски.
    :param mask_path: Путь к файлу с разметкой масок
    """

    with open(mask_path) as masks:
        images = os.listdir(original_images_path)
        soup = BeautifulSoup(masks, parser='xml', features='lxml')
        for image_name in images:
            tag = get_image_tag(image_name, soup)
            original_img = Image.open(f'{original_images_path}/{image_name}').copy()
            polygon_for_one_img = tag.find_all()
            coordinates = get_coordinates(polygon_for_one_img)

            # RGB - для сохранения маски на черном фоне,
            # RGBA - для наложения маски на изображение
            mask_im_rgb = Image.new('RGB', original_img.size, 0)
            mask_im_rgba = Image.new('RGBA', original_img.size)
            image_rgb = ImageDraw.Draw(mask_im_rgb)
            image_rgba = ImageDraw.Draw(mask_im_rgba)
            draw_polygon(coordinates, image_rgb, image_rgba)

            # Сохраняем новую маску и фото с наложенной маской.
            # Названия файлов содержат префиксы mask_ и with_mask_ соответственно
            mask_im_rgb.save(f'{new_images_path}/mask_{image_name}', format='jpeg')
            original_img.paste(mask_im_rgba, (0, 0), mask_im_rgba)
            name = image_name.split('.')[-2]
            original_img.save(f'{new_images_path}/with_mask_{name}.png', format='png')
            original_img.close()


if __name__ == '__main__':
    main(
        original_images_path='images',
        new_images_path='new_images',
        mask_path='masks.xml'
    )

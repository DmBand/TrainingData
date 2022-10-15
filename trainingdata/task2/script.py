import os

from bs4 import (BeautifulSoup,
                 Tag,
                 ResultSet)
from PIL import Image, ImageDraw


def get_image_tag(name: str, bs: BeautifulSoup) -> Tag:
    """
    Возвращает тег изображения,
    имя которого соответствует параметру "name"
    """

    for image_tag in bs.find_all('image'):
        if name in image_tag['name']:
            return image_tag


def get_coordinates(figures: ResultSet) -> list:
    """
    Возвращает полный список координат
    для одного изображения
    """

    all_coordinates = []
    for figure in figures:
        one_figure_coordinates = []
        if figure['label'] == 'Ignore':
            continue
        else:
            coord = figure['points'].split(';')
            for value in coord:
                coord = tuple(map(lambda num: float(num), value.split(',')))
                one_figure_coordinates.append(coord)
            all_coordinates.append(one_figure_coordinates)
    return all_coordinates


def draw_polygon(points: list,
                 draw_rgb: ImageDraw,
                 draw_rgba: ImageDraw,
                 color: tuple = (162, 41, 232)) -> None:
    """
    Рисует два многоугольника по заданным координатам
    """

    for c in points:
        draw_rgb.polygon(c, fill=color)
        draw_rgba.polygon(c, fill=color)


def main(original_images_path: str,
         new_images_path: str,
         masks_path: str) -> None:
    """
    :param original_images_path: Путь к папке, в которой
    хранятся необработанные изображения.
    :param new_images_path: Путь к папке, в которой
    хранятся обработанные изображения и маски.
    :param masks_path: Путь к файлу с разметкой масок
    """

    with open(masks_path) as masks:
        images = os.listdir(original_images_path)
        soup = BeautifulSoup(masks, parser='xml', features='lxml')
        for image_name in images:
            tag = get_image_tag(image_name, soup)
            original_img = Image.open(f'images/{image_name}').copy()
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
            mask_im_rgb.save(f'{new_images_path}/mask_{image_name}.jpg')
            original_img.paste(mask_im_rgba, (0, 0), mask_im_rgba)
            original_img.save(f'{new_images_path}/with_mask_{image_name}.png')
            original_img.close()


if __name__ == '__main__':
    main('images', 'new_images', 'masks.xml')

import os

from bs4 import BeautifulSoup


def main(path: str, path_for_save: str = None) -> None:
    """
    Открывает файл, изменяет его и сохраняет в новый файл,
    добавляя к названию префикс "new_"
    :param path: Путь к оригинальному файлу.
    :param path_for_save: Путь, по которому необходимо
    сохранить новый файл. Если None, то файл будет сохранен
    в текущей директории
    """

    with open(path) as file:
        soup = BeautifulSoup(file, parser='xml', features='lxml')
        image_tag = soup.find_all('image')
        image_ids = [img['id'] for img in image_tag]

        position = -1
        for img in image_tag:
            img['id'] = image_ids[position]
            position -= 1
            current_name = img['name'].split('/')[-1]
            new_name = current_name.split('.')[0] + '.png'
            img['name'] = new_name

    name = os.path.basename(path)
    if path_for_save:
        new_path = f'{path_for_save}/new_{name}'
    else:
        new_path = f'new_{name}'

    with open(new_path, 'w') as new_file:
        new_file.write(soup.prettify())


if __name__ == '__main__':
    files = os.listdir('annotations')
    for f in files:
        main(
            path=f'annotations/{f}',
            path_for_save='new_annotations'
        )

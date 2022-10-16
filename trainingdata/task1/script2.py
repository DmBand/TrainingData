from bs4 import BeautifulSoup


def main(path: str) -> None:
    """
    Открывает файл и собирает из него данные.
    :param path: Путь к оригинальному файлу.
    """

    with open(path) as file:
        soup = BeautifulSoup(file, parser='xml', features='lxml')
        image_tag = soup.find_all('image')
        marked_up_images = [img for img in image_tag if img.find()]

        data = {}
        for tag in marked_up_images:
            for figure in tag.find_all():
                label = figure['label']
                if label in data:
                    data[label] += 1
                else:
                    data[label] = 1

        for item in data:
            print(f'{item}: {data[item]} фигур')


if __name__ == '__main__':
    files = [
        'annotations.xml',
        'annotations-2.xml',
        'annotations-3.xml'
    ]
    for f in files:
        print(f'\n------------- {f} -------------')
        main(path=f)

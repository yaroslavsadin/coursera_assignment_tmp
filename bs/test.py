import unittest
from bs4 import BeautifulSoup
from collections import Counter
import re


def parse(path_to_file):
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    # return [imgs, headers, linkslen, lists]
    counter = Counter()

    with open(path_to_file, 'r', encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')

    bodies = soup.find_all(
        lambda x: x.name == 'div' and x.get('id', None) == 'bodyContent')

    for body in bodies:
        for _ in body.find_all(lambda tag: tag.name == 'img'
                               and int(tag.get('width', 0)) >= 200):
            counter['imgs'] += 1

    headers = soup.find_all(lambda tag: re.match(r'^h[1-6]$', tag.name)
                            and tag.text[0] in 'ETC')

    for _ in headers:
        counter['headers'] += 1

    print(counter)


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    # unittest.main()
    test_cases = (
        ('wiki/Stone_Age', [13, 10, 12, 40]),
        ('wiki/Brain', [19, 5, 25, 11]),
        ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
        ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
        ('wiki/Spectrogram', [1, 2, 4, 7]),)

    for path, expected in test_cases:
        parse(path)

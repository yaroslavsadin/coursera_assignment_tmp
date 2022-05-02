import unittest
from bs4 import BeautifulSoup, Tag
import re


def count_imgs(root):
    imgs = root.find_all(lambda tag: tag.name == 'img'
                         and int(tag.get('width', 0)) >= 200)
    return len(imgs)


def count_headers(root):
    headers = root.find_all(lambda tag: re.match(r'^h[1-6]$', tag.name)
                            and tag.text[0] in 'ETC')

    return len(headers)


def next_tag(root):
    sibling = root.next_sibling
    while sibling is not None and not isinstance(sibling, Tag):
        sibling = sibling.next_sibling
    return sibling


def count_refs(root):
    refs = root.find_all('a')
    longest = 0
    for ref in refs:
        next_tag = next_tag(ref)
        count = 1
        while next_tag and next_tag.name == 'a':
            count += 1
            next_tag = next_tag(next_tag)
        longest = max(longest, count)
    return longest


def count_lists(root):
    lists = root.find_all(['ul', 'ol'])
    count = 0
    for list_ in lists:
        for parent in list_.parents:
            if parent.name == 'li':
                break
        else:
            count += 1
    return count


def parse(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')

    body = soup.find(
        lambda x: x.name == 'div' and x.get('id', None) == 'bodyContent')

    res = [count_imgs(body), count_headers(body),
           count_refs(body), count_lists(body)]

    print(res)
    return res


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

import unittest
from bs4 import BeautifulSoup, Tag
import re


def parse(path_to_file):
    imgs_cnt = 0
    headers_cnt = 0
    linkslen_cnt = 0
    lists_cnt = 0

    with open(path_to_file, 'r', encoding='utf-8') as html:
        soup = BeautifulSoup(html, 'lxml')

    body = soup.find(
        lambda x: x.name == 'div' and x.get('id', None) == 'bodyContent')

    for _ in body.find_all(lambda tag: tag.name == 'img'
                           and int(tag.get('width', 0)) >= 200):
        imgs_cnt += 1

    headers = body.find_all(
        lambda tag: re.match(r'^h[1-6]$', tag.name) and tag.text[0] in 'ETC')

    for _ in headers:
        headers_cnt += 1

    refs = body.find_all('a')

    def next_sibling_tag(root):
        sibling = root.next_sibling
        while sibling is not None and not isinstance(sibling, Tag):
            sibling = sibling.next_sibling
        return sibling

    longest = 0

    for ref in refs:
        next_tag = next_sibling_tag(ref)
        count = 1
        while next_tag and next_tag.name == 'a':
            count += 1
            next_tag = next_sibling_tag(next_tag)
        longest = max(longest, count)

    linkslen_cnt = longest

    lists = body.find_all(['ul', 'ol'])

    count = 0
    for list_ in lists:
        for parent in list_.parents:
            if parent.name == 'li':
                break
        else:
            count += 1

    lists_cnt = count

    print([imgs_cnt, headers_cnt, linkslen_cnt, lists_cnt])

    return [imgs_cnt, headers_cnt, linkslen_cnt, lists_cnt]


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

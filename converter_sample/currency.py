from bs4 import BeautifulSoup
from decimal import Decimal


def currency_to_rub(soup, currency):
    if currency == 'RUR':
        return Decimal(1.)
    tag = soup.find(lambda x: x.name == 'CharCode' and x.text == currency)
    nominal = Decimal(tag.parent.find('Nominal').text.replace(',', '.'))
    return Decimal(tag.parent.find('Value').text.replace(',', '.')) / nominal


def convert(amount, cur_from, cur_to, date, requests_):
    response = requests_.get(
        f'https://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date})
    soup = BeautifulSoup(response.content, 'xml')

    from_ = currency_to_rub(soup, cur_from) * amount
    to = currency_to_rub(soup, cur_to)

    return round(from_ / to, 4)


if __name__ == '__main__':
    print(convert(Decimal(str(10 ** 3)), 'EUR', 'USD', "26/02/2017", None))

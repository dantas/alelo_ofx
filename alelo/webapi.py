import requests
import base64


session = requests.Session()


class WebApiFailure(Exception):
    pass


def login(cpf, password):
    result = session.post('https://www.meualelo.com.br/meualelo.services/rest/login/authenticate', json={
        'cpf': cpf,
        'pwd': base64.b64encode(password),
        'captchaResponse': '',
    })
    if result.status_code != 200:
        raise WebApiFailure()


def transactions(card_id, stard_date, end_date):
    result = session.get('https://www.meualelo.com.br/meualelo.services/rest/user/card/movement', params={
        'selectedCardNumberId': card_id,
        'startDate': stard_date,
        'endDate': end_date,
    })
    if result.status_code != 200:
        raise WebApiFailure()
    return result.content


def credentials():
    result = session.get('https://www.meualelo.com.br/meualelo.services/rest/login/credentials')
    if result.status_code != 200:
        raise WebApiFailure()
    return result.content


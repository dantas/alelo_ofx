from datetime import date, datetime
import calendar
import json
import re

import webapi


def fetch_transactions(cpf, password, card_number, month):
    webapi.login(cpf, password)

    card_id = _fetch_card_id(card_number)

    today = date.today()

    if type(month) == int and today.month != month:
        start_date = date(today.year, month, 1)
        end_date = date(today.year, month,
            calendar.monthrange(today.year, month)[1])
    else:
        start_date = today.replace(day=1)
        end_date = today

    transactions = webapi.transactions(card_id,
        start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"))

    return [_parse_transaction(t) for t in json.loads(transactions)["movements"]]


def _fetch_card_id(card_number):
    return json.loads(webapi.credentials())['products'][card_number]['cards'][0]['cardId']


regex_amount = re.compile(".*R\$\s*(.*)")


def _parse_transaction(json_transaction):
    return {
        'date': datetime.strptime(json_transaction['date'], "%d/%m/%Y"),
        'amount': regex_amount.match(json_transaction['amount']).group(1).replace(',', '.'),
        'signal': '+' in json_transaction['amount'] and '+' or '-',
        'description': json_transaction['description'],
    }

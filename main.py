#!/usr/bin/env python

import argparse

import alelo
import config
import ofx


def ask_user(preferences = {}):
    def add_argument(name, help, **kwargs):
        kwargs['required'] = kwargs.get('required', not (name in preferences))
        kwargs['default'] = kwargs.get('default', preferences.get(name, None))
        parser.add_argument('--' + name, help=help, **kwargs)

    parser = argparse.ArgumentParser(description="Access MeuAlelo system to extract this month's operations")

    add_argument('cpf', "CPF with only numbers")
    add_argument('password', "Password used to access the system")
    add_argument('card', "Which card from the list we want to access", type=int, default=0)
    add_argument('save', "If present saves the provided configurations in an init file",
        required=False, action="store_true")
    add_argument('month', "Specify for which month transactions must be converted",
        required=False, type=int)

    return vars(parser.parse_args())


def save_if_necessary(preferences):
    if preferences['save']:
        del preferences['save']
        del preferences['month']
        config.save(preferences)


def load_preferences():
    preferences = config.read()
    preferences['month'] = None
    preferences['card'] = int(preferences['card'])
    preferences['save'] = False
    return preferences


if __name__ == '__main__':
    preferences = ask_user(load_preferences())
    transactions = alelo.fetch_transactions(preferences['cpf'],
        preferences['password'], preferences['card'], preferences['month'])
    print ofx.convert(transactions)
    save_if_necessary(preferences)

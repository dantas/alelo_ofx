import unicodedata

import dict2xml


def convert(transactions):
    return dict2xml.to_string(dict2xml.convert("OFX", {
        "BANKMSGSRSV1": {
            "STMTTRNRS": {
                "STMTRS": {
                    "BANKTRANLIST": [_convert_transaction(t) for t in transactions],
                },
            },
        },
    }))


def _convert_transaction(transaction):
    date = transaction['date'].strftime("%Y%m%d%H%M%S")
    return dict2xml.convert("STMTTRN", {
        "DTPOSTED": date,
        "FITID": date,
        "TRNAMT": transaction['signal'] + transaction['amount'],
        "MEMO": unicodedata.normalize('NFD',
            transaction['description']).encode('ascii', 'ignore'),
    })

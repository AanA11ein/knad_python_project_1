from services.api import do_get

async def fetch_currency(base, api_key) -> dict | str:
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}'
    try:
        data = await do_get(url)
        if data['result'] != 'success':
            raise Exception
    except Exception:
        data = f"Sorry, we can't get currency data"
    return data

def normalize_currency(data, base, syms):
    res = []

    for sym in syms.split(','):
        value = data['conversion_rates'].get(sym)
        if value:
            res.append(f'1 {base} is {value} {sym}')
        else:
            res.append(f'Currency {sym} not found')

    return '\n'.join(res)

from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

crypto = {
    "Bitcoin": "bitcoin",
    "Ethereum": "ethereum",
    "Tether": "tether",
    "Solana": "solana",
    "BNB": "binancecoin",
    "XRP": "ripple",
    "Cardano": "cardano",
    "Dogecoin": "dogecoin",
}

currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'RUB': 'Российский рубль',
}


def update_crypto_label(event):
    code = crypto_combobox.get()
    name = currencies[code]
    crypto_label.config(text=name)


def update_currency_label(event):
    code = currency_combobox.get()
    name = currencies[code]
    currency_label.config(text=name)


def show_price():
    crypto_code = crypto_combobox.get().strip()
    currency_code = currency_combobox.get().strip()
    if (crypto_code and currency_code):
        try:

            response1 = requests.get(f'https://open.er-api.com/v6/latest/{currency_code}')
            response1.raise_for_status()
            data1 = response1.json()

            if crypto_code in data['rates']:
                exchange_rate1 = data['rates'][crypto_code]
                currency = currencies[currency_code]
                crypto = currencies[crypto_code]

                mb.showinfo('Курс обмена',
                            f'Курс: {exchange_rate} 1 {crypto} = {currency}')
            else:
                mb.showerror('Ошибка',
                             f'Валюта {crypto_code} не найдена')
        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Введите код валюты')


root = Tk()
root.title('Курс криптовалют')
root.geometry('360x280')

Label(root, text='Криптовалюта').pack()
crypto_combobox = ttk.Combobox(root, values=list(currencies.keys()))
crypto_combobox.pack(pady=4, padx=10)
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)
crypto_label = ttk.Label()
crypto_label.pack()

Label(root, text='Bалюта').pack(padx=10)
currency_combobox = ttk.Combobox(root, values=list(currencies.keys()))
currency_combobox.pack(pady=4, padx=10)
currency_combobox.bind('<<ComboboxSelected>>', update_currency_label)
currency_label = ttk.Label()
currency_label.pack()

Button(text='Показать курс', command=show_price).pack(pady=10, padx=10)
root.mainloop()

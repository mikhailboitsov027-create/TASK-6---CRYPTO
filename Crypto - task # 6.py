from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

crypto = {
    'Bitcoin': 'bitcoin',
    'Ethereum': 'ethereum',
    'Tether': 'tether',
    'Solana': 'solana',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'Cardano': 'cardano',
    'Dogecoin': 'dogecoin',
}

currencies = {
    'EUR': 'Евро',
    'USD': 'Доллар США',
    'RUB': 'Российский рубль',
}

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def update_crypto_label(event):
    code = crypto_combobox.get()
    name = crypto[code]
    crypto_label.config(text=name)


def update_currency_label(event):
    code = currency_combobox.get()
    name = currencies[code]
    currency_label.config(text=name)


def show_price():
    crypto_name = crypto_combobox.get().strip()
    currency_code = currency_combobox.get().strip()

    if crypto_name and currency_code:
        try:
            crypto_code = crypto[crypto_name]

            params = {
                'ids': crypto_code,
                'vs_currencies': currency_code.lower()
            }

            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if crypto_code in data and currency_code.lower() in data[crypto_code]:
                exchange_rate = data[crypto_code][currency_code.lower()]
                crypto_display = crypto_name
                currency_display = currencies[currency_code]

                mb.showinfo('Курс обмена', f'Курс: 1 {crypto_display} = {exchange_rate} {currency_display}')
            else:
                mb.showerror(
                    'Ошибка',
                    f'Курс для {crypto_name} в {currency_code} не найден'
                )

        except Exception as er:
            mb.showerror('Ошибка', er)

    else:
        mb.showwarning('Внимание', 'Выберите криптовалюту и валюту')


root = Tk()
root.title('Курс криптовалют')
root.geometry('360x280')

Label(root, text='Криптовалюта').pack()
crypto_combobox = ttk.Combobox(root, values=list(crypto.keys()))
crypto_combobox.pack(pady=4, padx=10)
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)
crypto_label = ttk.Label(root)
crypto_label.pack()


Label(root, text='Валюта').pack(padx=10)
currency_combobox = ttk.Combobox(root, values=list(currencies.keys()))
currency_combobox.pack(pady=4, padx=10)
currency_combobox.bind('<<ComboboxSelected>>', update_currency_label)
currency_label = ttk.Label(root)
currency_label.pack()


Button(root, text='Показать курс', command=show_price).pack(pady=10, padx=10)


#icon_path = r"C:\Users\User\Downloads\obmen_endqu872i8mh.ico"
#root.iconbitmap(icon_path)

root.mainloop()

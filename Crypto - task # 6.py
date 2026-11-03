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

currency_symbols = {
    'EUR': '€',
    'USD': '$',
    'RUB': '₽',
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

                symbol = currency_symbols.get(currency_code, currency_code)
                # Обновляем метку с курсом вместо всплывающего окна: mb.showinfo('Курс обмена', f'Курс: 1 {crypto_display} = {exchange_rate} {currency_display}')
                price_label.config(
                    text=f'Курс: 1 {crypto_display}  =  {symbol} {exchange_rate}'
                )

            else:
                mb.showerror(
                    'Ошибка',
                    f'Курс для {crypto_name} в {currency_code} не найден'
                )

        except Exception as er:
            mb.showerror('Ошибка', str(er))

    else:
        mb.showwarning('Внимание', 'Выберите криптовалюту и валюту')


root = Tk()
root.title('Курс криптовалют')
root.geometry('300x300')
root.config(bg='grey11')

blank = PhotoImage(width=1, height=1)
root.iconphoto(False, blank)

# --- ВИДЖЕТЫ  ---

# Заголовки колонок
Label(root, text='Криптовалюта', font=('Arial', 10, 'bold'), fg='white', bg='grey11').grid(row=0, column=0, padx=10,
                                                                                           pady=5, sticky='w')
Label(root, text='Валюта', font=('Arial', 10, 'bold'), fg='white', bg='grey11').grid(row=0, column=1, padx=10, pady=5,
                                                                                     sticky='w')

# Комбобоксы
crypto_combobox = ttk.Combobox(root, values=list(crypto.keys()), width=18)
crypto_combobox.grid(row=1, column=0, padx=10, pady=4)
crypto_combobox.bind('<<ComboboxSelected>>', update_crypto_label)

currency_combobox = ttk.Combobox(root, values=list(currencies.keys()), width=18)
currency_combobox.grid(row=1, column=1, padx=10, pady=4)
currency_combobox.bind('<<ComboboxSelected>>', update_currency_label)

# Подписи с названиями (под комбобоксами)
crypto_label = Label(root, text='', font=('Arial', 9), bg='grey11', fg='white')
crypto_label.grid(row=2, column=0, padx=10, pady=2, sticky='w')

currency_label = Label(root, text='', font=('Arial', 9), bg='grey11', fg='white')
currency_label.grid(row=2, column=1, padx=10, pady=2, sticky='w')

# Кнопка по центру
Button(root, text='•   Показать курс', command=show_price, width=20, bg="DarkGoldenrod4", font=('Arial', 10, 'bold'),
       fg="yellow").grid(row=3, column=0, columnspan=2, pady=15)

price_label = Label(root, text='', bg='grey11', fg='green1', font=('Arial', 13, 'bold'), anchor='center',
                    wraplength=400)
price_label.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()


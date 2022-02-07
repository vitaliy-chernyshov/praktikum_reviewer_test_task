# Общеее по репозитарию: в репозитарии не хватает папки или файла с тестами.
# так же не хватает файла .gitignore
# можно использовать заготовку из гитхаба для python куда уже включены папки
# venv, и всякое ненужное в гите.
# https://github.com/github/gitignore/blob/main/Python.gitignore

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            # формат даты можно вынести в константу, вдруг изменится?
            # легче найти и изменить будет в дальнейшем, чем искать в коде
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # во первых Record уже используется как название класса
        # во вторых имена переменных должны начинаться с маленькой буквы.
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # можно использовать сокращенный синтаксис присваивания
                # today_stats += something
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            # 1. можно использовать двойное сравнение, будет более читаемо:
            # 0 <= some_variable < 7
            # 2. вычисление (today - record.date).days идет два раза подряд.
            # стоит вынести в переменную.

            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # комментарии к классам, методам стоит оформить как docstrings
    # тогда они будут доступны в IDE
    # https://www.python.org/dev/peps/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # 1. однобуквенная переменнная - не очевидно для чего она используется
        # 2. вычисление self.limit - self.get_today_stats() используется в
        # нескольких местах. Следуя принципу DRY стоит вынести в отдельный метод
        # в базовом классе калькулятора (он используется в обоих калькуляторах)
        x = self.limit - self.get_today_stats()
        if x > 0:
            # 1. бекслеши не используем.
            # 2. В первой строке не используется подстановки, поэтому
            # f-строка лишняя
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # скобки тут не нужны, т.к. нет объединения строк
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    # 1. по заданию Метод get_today_cash_remained(currency) денежного
    # калькулятора должен принимать на вход код валюты: одну из строк "rub",
    # "usd" или "eur" и исходя из кода вылюты выдавать результат.
    # 2. даже если бы такого условия не было, аргументы функции стоило называть
    # c маленькой буквы
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Слишком много условий. Сейчас у нас 3 валюты, а что будет когда
        # попросят добавить еще десяток? Стоит сделать словарь с валютами.
        # Ключом этого словаря может быть код валюты, он уникальный.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # в условии используется сравнение, вероятно имелось в виду
            # присвоение
            cash_remained == 1.00
            currency_type = 'руб'

        # опять слишком много if .. else но словарем тут не обойтись. Рекомендую
        # https://refactoring.guru/ru/replace-nested-conditional-with-guard-clauses
        # стоит добавить guard block и убрать лишние if elif
        if cash_remained > 0:
            # в f-строках не должно быть никаких вычислений
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        # стоит использовать эту проверку первой. Если денег нет то и
        # дальнейшие вычисления не нужны. 
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            # бекслеш, см выше, вычисление в f-строке
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # в этой строке ничего не переопределается, при наследовании от
    # родительского класса все методы так же наследуются. Поэтому этот метод
    # тут лишний
    def get_week_stats(self):
        super().get_week_stats()
        
# не хватает проверки базовой функциональности - создать пару калькуляторов,
# добавить записи, посмотреть что на выходе. Такую проверку стоит выносить
# отдельно в конструкцию if __name__ == '__main__': чтобы она не выполнялась
# при импорте а только при явном запуске.
# https://pyneng.readthedocs.io/ru/latest/book/11_modules/if_name_main.html

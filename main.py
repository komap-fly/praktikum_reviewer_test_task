import datetime as dt
import json # импорт не используется
# PEP 8: должны быть 2 пустые линии, вместо одной
class Record:
    def __init__(self, amount, comment, date=''):
        self.amount=amount  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        self.date = dt.datetime.now().date() if not date else dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment=comment  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
class Calculator:  # PEP 8: E302 перед классом должно быть 2 пустые линии
    def __init__(self, limit):
        self.limit = limit
        self.records=[]  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
    def add_record(self, record):  # PEP 8: E301 должна быть 1 пустая линия перед методом
        self.records.append(record)
    def get_today_stats(self):  # PEP 8: E301 должна быть 1 пустая линия перед методом
        today_stats=0  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        for Record in self.records:  # Сразу две ошибки, во-первых, мы создаем локально переменную, которая определена глобально(Record), во-вторых, по PEP8 имена переменны задаются snake_case, а не CamelCase
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats+Record.amount  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        return today_stats
    def get_week_stats(self):  # PEP 8: E301 должна быть 1 пустая линия перед методом
        week_stats=0  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        today = dt.datetime.now().date()
        for record in self.records:
            if (today -  record.date).days <7 and (today -  record.date).days >=0:
                # следует упростить выражение сверху
                # во-первых, (today - record.date).days вычисляется 2 раза, следует вычислить один раз и записать в переменную
                # во вторых, убрать and из логического выражения и заменить на более простое выражение:
                # пример: Было if x < A and x >= B -> if B <= x < A:
                # можно также переписать через range функцию и оператор in
                week_stats +=record.amount  # PEP 8: E225 оператор должен быть отделен пробелам (x += y)
        return week_stats
class CaloriesCalculator(Calculator):
    '''
    Во-первых, комментарий "Получает остаток калорий на сегодня" должен был быть отделен 2 пробелами
    Во-вторых, комментарий избыточен, название метода говорит само за себя
    '''
    def get_calories_remained(self): # Получает остаток калорий на сегодня
        x=self.limit-self.get_today_stats()  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        # Название перменной (x) должно быть содержательным и не состоят из одной буквы
        if x > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {x} кКал'
        else:
            return 'Хватит есть!'
class CashCalculator(Calculator):
    '''
    По поводу USD_RATE и EURO_RATE констант
    Во-первых, комментарии избыточны, названия USD_RATE и EURO_RATE прекрасно
    отображают назначение переменных
    Во-вторых, так как важна точность вычислений,
    следует применять класс Decimal(from decimal import Decimal)
    для большей точности вычислений)
    '''
    USD_RATE=float(60) #Курс доллар США.
    EURO_RATE=float(70) #Курс Евро.
    '''
    В методе get_today_cash_remained имеется ряд ошибок.
    Во-первых, нарушен PEP8:
        перед методом должен быть один отступ
        названия аргументов должны быть в нижнем регистре
    Во-вторых, не выбрасывается исключение, если currency не является одним из ["usd", "eur", "rub"]
    Соответственно, возникает неожиданный вывод
    >>> calculator = CashCalculator(limit=100)
    >>> calculator.get_today_cash_remained('')
    'На сегодня осталось 100 '
    '''
    def get_today_cash_remained(self, currency, USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type=currency
        cash_remained = self.limit - self.get_today_stats()
        if currency=='usd':  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
            cash_remained /= USD_RATE
            currency_type ='USD'  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        elif currency_type=='eur':  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
            cash_remained /= EURO_RATE
            currency_type ='Euro'  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        elif currency_type=='rub':  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
            cash_remained == 1.00  # нет смысла в этой строке, можно удалить
            currency_type ='руб'  # PEP 8: E225 оператор должен быть отделен пробелам (x = y)
        if cash_remained > 0:
            return f'На сегодня осталось {round(cash_remained, 2)} {currency_type}'  #  Не использовать операции в f строках
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(-cash_remained, currency_type)
    '''
    в переопределении методе get_week_stats нет смысла,
    так как вызывается метод родительского класса без изменений, следует удалить
    '''
    def get_week_stats(self):
        super().get_week_stats()
'''
Замечания в целом
Несколько раз вызывается dt.datetime.now().date(),
следует вынести вызов функции в отдельную функцию,
чтобы уменьшить дублирование

2 раза вызывается self.limit-self.get_today_stats()
следует вынести данный функционал в базовый класс
'''
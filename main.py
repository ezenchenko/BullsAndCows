"""
В классическом варианте игра рассчитана на двух игроков. Каждый из игроков задумывает и записывает тайное 4-значное число с неповторяющимися цифрами.
Игрок, который начинает игру по жребию, делает первую попытку отгадать число. Попытка — это 4-значное число с неповторяющимися цифрами, сообщаемое противнику.
Противник сообщает в ответ, сколько цифр угадано без совпадения с их позициями в тайном числе (то есть количество коров)
и сколько угадано вплоть до позиции в тайном числе (то есть количество быков). Например:

Задумано тайное число «3219».
Попытка: «2310».
Результат: две «коровы» (две цифры: «2» и «3» — угаданы на неверных позициях) и один «бык» (одна цифра «1» угадана вплоть до позиции).

Игроки начинают по очереди угадывать число соперника. Побеждает тот, кто угадает число первым, при условии, что он не начинал игру.
Если же отгадавший начинал игру — его противнику предоставляется последний шанс угадать последовательность.
"""
from random import randint

class BC(object):
    """
        порядок работы с объектом

        1 b=BC()
        2 guess = b.first_step() #первый шаг вернет число первой попытки
        3 b.answer(cows, bulls)  #передаем ответ сколько коров и быков (для автоматизации подсчета можно использовать cows, bulls = b.calc_bc(secret_val, guess) )
        4 guess = b.next_step()  #генереруем следующую догадку
        5 b.answer(cows, bulls)  #передаем ответ сколько коров и быков
        ....

        Повторяем 4,5 шаги пока не будет надпись "Ура отгадал это: ..."

    """


    def __init__(self):
        self.solutions = self.create_pull_solution() #все возможные комбинации решений, кстати их всего 5039 для цифр от 0 - 9
        self.guess = {} #Массив догадок key = цифра догадка val = (c, b) оценка догадки в коровах и быках


    def first_step(self): #первый шаг
        self.solutions = self.create_pull_solution() #все возможные комбинации решений, кстати их всего 5039 для цифр от 0 - 9
        self.guess = {} #Массив догадок key = цифра догадка val = (c, b) оценка догадки в коровах и быках
        self.curr_guess = self.solutions[randint(0, len(self.solutions)-1)]  # Начальная догадка
        return self.curr_guess

    def answer(self, c, b):
        if b == 4 and c == 0:
            print(f'Ура отгадал это: {self.curr_guess}')
            return True
        self.guess[self.curr_guess] = (c, b)
        return False

    def next_step(self):
        """
        1. Обрезаем варианты ответов
        2. Генерируем догадку

        :return: догадка str
        """
        cs = self.trim_solution()
        self.curr_guess = self.generate_guess_rnd(cs)
        return self.curr_guess


    def generate_guess_rnd(self, cs):
        """
        В простейшем случае генерируем следующую попытку случайным числом из числа возможных вариантов
        :param cs: array возможных комбинаций
        :return: str число для следующей попытки
        """
        return cs[randint(0, len(cs)-1)]


    def create_pull_solution(self) -> []:
        """
            Создание всех возможных комбинаций решений
        """
        ret = []
        for i in range(123,9876):
            s_num = f'{i:04}'
            if self.is_right_num(s_num):
                ret.append(s_num)
        return ret

    def is_right_num(self, s_num):
        """
            Проверка на не повторяемость цифр
        """
        if len([item for item in '0123456789' if item not in s_num]) == 6:
            return True
        return False

    def trim_solution(self):
        """
            Удаляем из решений те которые не соответствуют результату в быках и коровах, перебирая все ранее предложенные варианты.
            Возвращаем список вариантов с подходящими оценками.
        """
        clues = self.solutions

        for c_sol, c_bc in self.guess.items():
            clues = [sol for sol in clues if c_bc == self.calc_bc(sol, c_sol)]
        return clues

    def calc_bc(self, secret_val:str, attempt_val:str):
        """
            Вычисляем число в быках и коровах
            secret_val - секретное число
            attempt_val - число догадка
            Возвращаем (быки, коровы)
        """

        def calc_bulls(sv, c_guess): #Вычисляем быков
            return len([c for i, c in enumerate(sv) if c_guess[i] == sv[i]]) #количество одинаковых цифр стоящих на одинаковых позициях


        def calc_cows(sv, c_guess): #Вычисляем коров
            return len([c for c in c_guess if c in sv]) - calc_bulls(sv, c_guess) #общее количество найденных цифр минус количество цифр стоящих на месте


        return (  calc_cows(secret_val, attempt_val), calc_bulls(secret_val, attempt_val) )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """
        Решение логической головоломки Быки и Коровы
    """
    secret_val = '4573'
    print(f'Загадано: {secret_val}')
    b = BC()
    guess = b.first_step()  # первый шаг вернет число первой попытки
    print(f'Это {guess}', end=' ')
    cows, bulls = b.calc_bc(secret_val, guess)
    print(f'Ответ {cows}:{bulls}')
    while not b.answer(cows, bulls):  # передаем ответ сколько коров и быков (для автоматизации подсчета можно использовать cows, bulls = b.calc_bc(secret_val, guess) )
        guess = b.next_step()  # генереруем следующую догадку
        print(f'Это {guess}', end=' ')
        cows, bulls = b.calc_bc(secret_val, guess)
        print(f'Ответ {cows}:{bulls}')



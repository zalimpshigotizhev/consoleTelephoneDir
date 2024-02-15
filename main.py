import csv
import os
import time


def clear_cmd():
    """ Очищает консоль. """
    os.system("cls" if os.name == "nt" else "clear")


def separator(symbol="*", total_time=2):
    """ Отрисовывает разделительную линию.
        - Дает время для чтения информации
         - Символ по умолчанию - "*"
         - Время по умолчанию - 2
    """
    print(symbol * 3)
    time.sleep(total_time / 3)
    print(symbol * 6)
    time.sleep(total_time / 3)
    print(symbol * 9)
    time.sleep(total_time / 3)


class Data:
    """ Класс для работы с данными.
        Принимает только адрес файла.
        - Сортирует данные по возрастанию
        - Сохраняет отсортированные данные
    """
    def __init__(self, url, data=None) -> None:
        """
        url - адрес файла
        title - заголовки
        data - данные из файла
        sorted_data - Функция которая сортирует данные
        page - текущая страница
        start - с какого элемента начать вывод (пагинация)
        limit - сколько элементов вывести (пагинация)
        """
        self.url = url

        if data:
            self.data = data
        else:
            self.data = self.get_data()
        self.sorted_data()
        self.title = self.get_title()
        self.page = 0
        self.start = 0
        self.limit = 5

    def get_title(self):
        """ Возвращает заголовки. """
        with open(self.url, "r", encoding="utf-8") as f:
            all_data = list(csv.reader(f))
        return all_data[0]

    def check_sorted_data(self, listt):
        """ Проверяет отсортирован ли список. """
        return all(listt[i] <= listt[i+1] for i in range(len(listt) - 1))

    def get_data(self):
        """ Возвращает данные. """
        with open(self.url, "r", encoding="utf-8") as f:
            all_data = list(csv.reader(f))
            self.title = all_data[0]
        return all_data[1:]

    def sorted_data(self, data=None):
        """ Сохраняет отсортированные данные.
            В начале она проверяет отсортированны ли данные,
            если нет, то сортирует.
        """
        if self.check_sorted_data(self.data) is False:
            fieldnames = self.title
            with open(self.url, "w", encoding="utf-8", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                sort_data = sorted(self.data)
                for row in sort_data:
                    row = [i.strip() for i in row]
                    writer.writerow(dict(zip(fieldnames, row)))
                self.data = sort_data

    def __iter__(self):
        """ Возвращает объект для перебора. """
        return self

    def __next__(self):
        """ Возвращает следующую страницу. """
        if self.start < len(self.data):
            self.start += self.limit
            self.page += 1
            return self.data[self.start:self.start + self.limit]
        raise StopIteration

    def back(self):
        """ Возвращает предыдущую страницу.
            Мы просто работаем с итератором, чтоб достичь
            предыдущей страницы.
        """
        if self.page > 1:
            self.page -= 2
            self.start -= (self.limit * 2)

    def restart_data(self):
        """ Возвращает данные в исходное состояние.
            - Это вызывается при выходе из контекста.
        """
        self.page = 0
        self.start = 0
        self.limit = 5

    def edit_person(self, person_indx):
        """ Изменяет данные человека по выбору.
            - person_indx - индекс человека в списке.
              (находит с помощью search_person)
        """
        while True:
            print("Что именно вы бы хотели изменить?")
            print("1. Фамилию")
            print("2. Имя")
            print("3. Отчество")
            print("4. Личный номер телефона")
            print("5. Компанию")
            print("6. Номер телефона компании")
            print("7. Выход")

            choice = int(input())

            if choice == 1:
                self.data[person_indx][0] = input(
                    "Новая фамилия: "
                )
            elif choice == 2:
                self.data[person_indx][1] = input(
                    "Новое имя: "
                )
            elif choice == 3:
                self.data[person_indx][2] = input(
                    "Новое отчество: "
                )
            elif choice == 4:
                self.data[person_indx][3] = input(
                    "Новый личный номер телефона: "
                )
            elif choice == 5:
                self.data[person_indx][4] = input(
                    "Новая компания: "
                )
            elif choice == 6:
                self.data[person_indx][5] = input(
                    "Новый номер телефона компании: "
                )
            elif choice == 7:
                break
            self.sorted_data()
            print("Данные успешно изменены!")
            separator()
            return

    def special_binary_search(self, data, indx, obj_search):
        """ Бинарный поиск. Находит однофамильцев.
            Из измененного:
            - При нахождении нужной фамилии он ищет
            рядом такую же, чтобы собрать в списке
            индексы всех однофамильцев.
        """
        low = 0
        high = len(data) - 1
        listt = []

        while low <= high:
            mid = (low + high) // 2
            if data[mid][indx] == obj_search:
                while data[mid][indx] == obj_search:
                    listt.append(mid)
                    if (data[mid - 1][indx] == obj_search and
                            data[mid - 1] not in listt):
                        mid -= 1
                    elif (data[mid + 1][indx] == obj_search and
                          data[mid + 1] not in listt):
                        mid += 1
                    else:
                        return listt
            elif data[mid][indx] < obj_search:
                low = mid + 1
            else:
                high = mid - 1

        return listt

    def search_person_algorithm(self, search):
        """ Алгоритм поиска.
            1) Находит однофамильцев.
            2) Если они есть, то ищет того с подходящим именем и отчеством.
        """
        last_name, first_name, patronymic = search.split()
        result_last_name_indxs = self.special_binary_search(
            self.data, 0, last_name
        )
        result = []

        for person in result_last_name_indxs:
            if (self.data[person][1] == first_name and
                    self.data[person][2] == patronymic):
                result.append(person)

        return result

    def add_person(self):
        """ Интерфейс.
            Добавление человека.
        """
        while True:
            clear_cmd()
            print()

            print("\033[44m", "Добавление человека:", "\033[0m")
            print()
            print("Если вам неизвестно что либо из графов, " +
                  "введите вместо этого прочерк.")
            print()
            print("Пустая строка и " + "\033[44m" + "⎆ENTER" +
                  "\033[0m" + " для выхода")

            last_name = input("Фамилия: ")
            if last_name == "":
                break
            first_name = input("Имя: ")
            if first_name == "":
                break
            patronymic = input("Отчество: ")
            if patronymic == "":
                break
            personal_number = input("Личный номер телефона: ")
            if personal_number == "":
                break
            company = input("Компания: ")
            if company == "":
                break
            company_number = input("Номер телефона компании: ")
            if company_number == "":
                break
            new = [
                last_name,
                first_name,
                patronymic,
                company,
                company_number,
                personal_number
            ]
            self.data.append(new)
            self.sorted_data()

    def search_person(self):
        """ Интерфейс.
            Поиск человека по ФИО.
        """
        while True:
            clear_cmd()
            print()

            print("\033[44m", "Поиск по ФИО:", "\033[0m")
            print()
            print("\033[41m" +
                  "Важно: для поиска необходимо вводить ФИО," + "\n" +
                  "Но если вы не в курсе об одном или двух инициалах," + "\n" +
                  "то пожалуйста введите вместо этого прочерк." + "\n" +
                  "Пример: Иванов - -", "\033[0m")
            print()
            print("Пустая строка и " + "\033[44m" + "⎆ENTER" +
                  "\033[0m" + " для выхода")

            search = input("\033[44m Поиск:\033[0m  ")

            if search == "":
                break

            if len(search.split(' ')) != 3:
                print("Некорректный ввод!")
                print("\033[43m", "Пример:", "\033[0m",
                      "\033[31;47m", "Иванов Иван Иванович", "\033[0m")
                separator()
                continue
            print()
            print()

            print("\033[32m", "Результаты поиска:", "\033[0m")
            person_indx = self.search_person_algorithm(search)

            if person_indx:
                indx = person_indx[0]
                while True:
                    print("\033[32m", "ФИО", "\033[0m",
                          self.data[indx][0],
                          self.data[indx][1],
                          self.data[indx][2])
                    print("\033[32m", "Личный номер телефона", "\033[0m",
                          self.data[indx][5])
                    print("\033[32m", "Компания", "\033[0m",
                          self.data[indx][3])
                    print("\033[32m", "Номер телефона компании", "\033[0m",
                          self.data[indx][4])
                    print()
                    print("\033[34m" + "1. Изменить данные\n" + "\033[0m" +
                          "\033[33m" + "2. Назад в поисковик\n" + "\033[0m" +
                          "\033[31m" + "3. Выход" + "\033[0m"
                          )
                    print()

                    nav = int(input())
                    if nav == 1:
                        self.edit_person(indx)
                    elif nav == 2:
                        break

            else:
                print("\033[31m", "Пользователь не найден", "\033[0m")
                print()
                separator()

    def present_list(self):
        """ Интерфейс.
            Показывает список людей.
        """
        while True:
            try:
                clear_cmd()
                page = self.__next__()
                print("\033[44m", "Номер_страницы:", self.page, "\033[0m")
                print()

                for i in page:
                    if len(i) != 1:
                        print("\033[32m", "ФИО", "\033[0m",
                              i[0], i[1], i[2])
                        print("\033[32m", "Личный номер телефона", "\033[0m",
                              i[5])
                        print("\033[32m", "Компания", "\033[0m",
                              i[3])
                        print("\033[32m", "Номер телефона компании", "\033[0m",
                              i[4])
                        print()

                print("\033[34m" + "1. Далее\n" + "\033[0m" +
                      "\033[33m" + "2. Назад\n" + "\033[0m" +
                      "\033[31m" + "3. Выход" + "\033[0m"
                      )
                nav = int(input())

                if nav == 2:
                    self.back()

                elif nav == 3:
                    self.restart_data()
                    return

                print("\033[31m", "Такого пункта нет", "\033[0m")

            except StopIteration:
                print("Достигнут конец списка")
                separator()
                self.restart_data()
                return


class Main:
    """ Главное меню. """
    def __init__(self) -> None:
        self.data = self.get_data()

    def get_data(self):
        """ Создание экземпляра.
            Возвращает экземпляр Data.
        """
        return Data("data/data.csv")

    def redirect_list_persons(self):
        """ Редирект к списку людей. """
        self.data.present_list()

    def redirect_find_person(self):
        """ Редирект к поиску людей. """
        self.data.search_person()

    def redirect_add_person(self):
        """ Редирект к добавлению людей. """
        self.data.add_person()

    def run(self):
        """ Основное меню. """
        while True:
            print("Выберите из следующих вариантов: \n" +
                  "1. Показать список людей \n" +
                  "2. Найти человека по ФИО \n" +
                  "3. Добавить человека в телефонную книгу \n")

            try:
                user_choice = int(input())
                if user_choice == 1:
                    self.redirect_list_persons()
                elif user_choice == 2:
                    self.redirect_find_person()
                elif user_choice == 3:
                    self.redirect_add_person()
                else:
                    print("Такого варианта нет")
                    separator("-", 1.5)
            except ValueError:
                print("Некорректный ввод! Пожалуйста, введите число.")
            clear_cmd()


if __name__ == "__main__":
    main = Main()
    clear_cmd()
    main.run()

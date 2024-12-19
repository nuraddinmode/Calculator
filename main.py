# Словари для чисел и операций
number_words = {  # Словарь для преобразования текстовых чисел в числовые значения
    "ноль": 0,
    "один": 1,
    "два": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
    "тридцать": 30,
    "сорок": 40,
    "пятьдесят": 50,
    "шестьдесят": 60,
    "семьдесят": 70,
    "восемьдесят": 80,
    "девяносто": 90
}

# Обратный словарь для преобразования чисел в текстовые значения
number_to_text = {}  # Пустой словарь для обратных пар
for word, value in number_words.items():  # Проходим по всем парам текст-число
    number_to_text[value] = word  # Меняем местами: число становится ключом, текст - значением
# print(number_to_text) # Проверили, что number_to_text(объект) заполняется

# Дополняем числа с десятками и единицами
for tens in [20, 30, 40, 50, 60, 70, 80, 90]:  # Перебираем десятки
    for ones in range(1, 10):  # Перебираем единицы
        combined_number = tens + ones  # Складываем десятки и единицы
        combined_text = f"{number_to_text[tens]} {number_to_text[ones]}"  # Формируем текстовое представление числа
        number_to_text[combined_number] = combined_text  # Сохраняем результат в словарь
# print(number_to_text) # Проверили, что number_to_text(объект) заполняется комбинированным

# Словарь операций
operations = {  # Преобразуем текстовые операции в символы
    "плюс": "+",
    "минус": "-",
    "умножить": "*"
}

# Указываем приоритет операций
priority = {
    "+": 1,  # Сложение и вычитание имеют одинаковый приоритет
    "-": 1,
    "*": 2   # Умножение имеет более высокий приоритет
}

# Преобразование текста в число
def text_to_number(text):
    """Преобразует текстовое представление числа в числовое значение."""
    parts = text.split()  # Разделяем текст на слова по пробелам
    result = 0  # Инициализируем результат
    for part in parts:  # Обрабатываем каждую часть текста
        if part in number_words:  # Если слово есть в словаре чисел
            result += number_words[part]  # Добавляем значение к результату
        else:  # Если слово не найдено
            raise ValueError(f"Не удалось распознать '{part}'")  # Выбрасываем ошибку
    return result  # Возвращаем итоговое число

# Преобразование выражения в список токенов
def tokenize(expression):
    """Преобразует текстовое выражение в список токенов (чисел и операций)."""
    tokens = []  # Список токенов
    words = expression.split()  # Разделяем выражение на слова по пробелу
    # print(words) # Проверили, что лежит в этом массиве
    i = 0  # Текущий индекс
    while i < len(words):  # Пока не обработаны все слова
        if words[i] in operations:  # Если слово — это операция
            if words[i] == "минус" and i + 1 < len(words) and words[i + 1] == "минус":  # Если встречается "минус минус"
                tokens.append("+")  # Заменяем "минус минус" на "+"
                i += 2  # Пропускаем оба "минус"
            else:  # Если обычная операция
                tokens.append(operations[words[i]])  # Добавляем символ операции
                i += 1
        elif words[i] == "на":  # Пропускаем "на" в выражениях
            i += 1
        else:  # Если это число
            start = i  # Начинаем собирать текст числа
            while i < len(words) and words[i] not in operations and words[i] != "на":  # Пока слово не операция
                i += 1
            number_text = " ".join(words[start:i])  # Объединяем слова в текст числа
            tokens.append(text_to_number(number_text))  # Преобразуем текст в число и добавляем в токены
    return tokens  # Возвращаем список токенов [5, '+', 2, '*', 3, '-', 1]

# Преобразование выражения в обратную польскую нотацию (ОПН)
def to_rpn(tokens):
    """Преобразует токены в обратную польскую нотацию (ОПН)."""
    output = []  # Итоговый список
    stack = []  # Стек для операций
    for token in tokens:  # Перебираем токены
        if isinstance(token, int):  # Если токен — число
            output.append(token)  # Добавляем его в выходной список
        else:  # Если токен — операция
            while stack and priority[token] <= priority[stack[-1]]:  # Пока приоритет выше или равен
                output.append(stack.pop())  # Перемещаем операцию из стека в выходной список
            stack.append(token)  # Кладём текущую операцию в стек
    while stack:  # Добавляем оставшиеся операции из стека в выходной список
        output.append(stack.pop())
    return output  # Возвращаем выражение в ОПН [5, 2, 3, '*', '+', 1, '-']

# Вычисление результата выражения в ОПН
def evaluate_rpn(rpn):
    """Вычисляет значение выражения в ОПН."""
    stack = []  # Стек для вычислений
    for token in rpn:  # Перебираем токены
        if isinstance(token, int):  # Если токен — число
            stack.append(token)  # Кладём число в стек
        else:  # Если токен — операция
            b = stack.pop()  # Извлекаем два числа из стека
            a = stack.pop()
            if token == "+":  # Если операция сложение
                stack.append(a + b)
            elif token == "-":  # Если операция вычитание
                stack.append(a - b)
            elif token == "*":  # Если операция умножение
                stack.append(a * b)
    return stack[0]  # Возвращаем результат = 10

# Основная функция
def calc(expression):
    """Выполняет вычисление текстового выражения."""
    try:
        tokens = tokenize(expression)  # Преобразуем выражение в токены = [5, '+', 2, '*', 3, '-', 1]
        rpn = to_rpn(tokens)  # Преобразуем токены в ОПН = [5, 2, 3, '*', '+', 1, '-']
        result = evaluate_rpn(rpn)  # Вычисляем результат = 10
        return number_to_text.get(result, str(result))  # Преобразуем результат в текстовое представление = 'десять'
    except ValueError as e:
        return f"Ошибка: {e}"  # Возвращаем сообщение об ошибке

# Тестовые примеры
print("Функция успешно реализована. Примеры выполнения:")
# print(f'calc("пятьдесят пять плюс двадцать") → "{calc("пятьдесят пять плюс двадцать")}"')  # Ожидаем "семьдесят пять"
# print(f'calc("пятьдесят три минус тринадцать") → "{calc("пятьдесят три минус тринадцать")}"')  # Ожидаем "сорок"
# print(f'calc("три умножить на десять") → "{calc("три умножить на десять")}"')  # Ожидаем "тридцать"
print(f'calc("пять плюс два умножить на три минус один") → "{calc("пять плюс два умножить на три минус один")}"')  # Ожидаем "десять"
# print(f'calc("двадцать плюс четыре умножить на пять минус два") → "{calc("двадцать плюс четыре умножить на пять минус два")}"')  # Ожидаем "тридцать восемь"
# print(f'calc("пять минус минус двадцать") → "{calc("пять минус минус двадцать")}"')  # Ожидаем "двадцать пять"
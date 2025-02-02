import data
import sender_stand_request
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body
def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Аа") # Создание тела запроса с именем пользователя из двух букв ("Аа").
    user_response = sender_stand_request.post_new_user(user_body) # Отправка запроса на создание нового пользователя с использованием модифицированного тела запроса.
    assert user_response.status_code == 201 # Проверка, что сервер отвечает с кодом состояния HTTP 201, что означает успешное создание ресурса.
    assert user_response.json()["authToken"] != "" # Проверка, что в ответе сервера есть поле authToken и оно не пустое — это подтверждает успешную регистрацию и выдачу токена авторизации.
    users_table_response = sender_stand_request.get_users_table() # Отправка запроса на получение списка всех пользователей из таблицы user_model.
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"] # Формирование строки, которая должна быть в ответе на запрос списка пользователей — в ней содержится информация о созданном пользователе и его токене авторизации.
    assert users_table_response.text.count(str_user) == 1 # Проверка, что строка с данными только что созданного
def get_user_body(first_name): # Отдельная функция positive_assert()\
    # Все позитивные проверки из чек-листа отличаются друг от друга только содержимым в поле first_name.
    # Поэтому повторяющиеся фрагменты удобнее вынести в отдельную функцию positive_assert() c входным параметром first_name
    # а внутри теста вызывать эту функцию с параметром Aa.
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body
# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

def test_create_user_15_letter_in_first_name_get_success_response():
        positive_assert("Aaaaaaaaaaaaaaa")

def negative_assert_symbol(first_name):    # Функция для негативной проверки
        # В переменную user_body сохраняется обновлённое тело запроса
        user_body = get_user_body(first_name)

        # В переменную response сохраняется результат запроса
        response = sender_stand_request.post_new_user(user_body)

        # Проверка, что код ответа равен 400
        assert response.status_code == 400

        # Проверка, что в теле ответа атрибут "code" равен 400
        assert response.json()["code"] == 400
        # Проверка текста в теле ответа в атрибуте "message"
        assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                             "Имя может содержать только русские или латинские буквы, " \
                                             "длина должна быть не менее 2 и не более 15 символов"
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")
def test_create_user_russian_letter_in_first_name_get_success_response():
        positive_assert("Мария")
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и КО")
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")
def negative_assert_no_first_name(user_body): #функция negative_assert_no_first_name(), которая на вход получает параметр user_body — тело для запроса на создание пользователя.
    response = sender_stand_request.post_new_user(user_body) #В поле response сохраняет ответ.
    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


    # В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
        # Копируется словарь с телом запроса из файла data в переменную user_body
        # Иначе можно потерять данные из исходного словаря
        user_body = data.user_body.copy()
        # Удаление параметра firstName из запроса
        user_body.pop("firstName")
        # Проверка полученного ответа
        negative_assert_no_first_name(user_body)

# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
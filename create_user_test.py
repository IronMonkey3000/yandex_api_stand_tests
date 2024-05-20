import sender_stand_request
import data
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
    assert users_table_response.text.count(str_user) == 1 # Проверка, что строка с данными только что созданного пользователя встречается в ответе на запрос списка пользователей ровно один раз, что подтверждает его уникальность и успешное добавление в систему.


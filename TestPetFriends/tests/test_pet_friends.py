from api import PetFriends
from env import valid_email, valid_password, incorrect_email, incorrect_password
import os

pf = PetFriends()

#Позитивные тесты

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Енот', animal_type='Звери',
                                     age='5', pet_photo='images/Racoon.jpeg'):
    """Проверяем, что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_update_self_pet_info(name='Енот', animal_type='Звери', age=3):
    """Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
         raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Лев", "кошачьи", "3", "images/Leon.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()



def test_create_pet_simple(name='Лев', animal_type='Кошки',age=4 ):
    """ Проверяем, что можно добавить питомца с корректными данными (без фото)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_set_photo_pets( pet_id = '58b070ea-fcc6-49ac-8154-6cad9bb91f0a', pet_photo='images/Leon.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.set_photo_pets(auth_key,pet_id, pet_photo)
    assert status == 200
    
    #Негативные тесты
    
def test_get_api_key_for_incorrect_user(email = incorrect_email , password = incorrect_password):
    """ Проверяем что запрос api ключа с некорректными email и password возвращает статус 403 """
    status, result = pf.get_api_key(email, password)
    assert status == 403

def test_add_new_pet_with_invalid_data(name='Енот', animal_type='Звери',
                                     age='5', pet_photo='images/Racoon.jpeg'):
    """Проверяем, что при отправке некорректных данных сервер отправляет код ошибки 400"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_with_invalid_data(auth_key, name, animal_type, age, pet_photo)
    assert status == 400

def test_create_pet_simple_with_invalid_data(name='Лев', animal_type='Кошки',age=4 ):
    """ Проверяем, что при отправке некорректных данных приходит код ошибки 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_with_invalid_data(auth_key, name, animal_type, age)
    assert status == 400









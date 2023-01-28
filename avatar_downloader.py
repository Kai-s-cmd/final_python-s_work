from YaUploader import YaUploader as Ya
import json
from token_vk import TOKEN
import requests


class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_user_photo(self):
        """Метод делает запрос к апи ВК и подгружает json с данными
         пользователя касающихся фото."""
        yandex_disk = Ya()
        fold_name = input('Введите название папки: ')
        yandex_disk.create_folder(fold_name)
        for user, id in self.id.items():
            url = 'https://api.vk.com/method/photos.get'
            params = {'owner_id': id,
                      'album_id': 'profile',
                      'photo_sizes': '1',
                      'extended': '1'}

            response = requests.get(url, params={**self.params, **params})
            profile_album = json.loads(response.text)
            try:
                items = profile_album['response']['items']
            except KeyError:
                print('Приватный профиль, загрузка не возможна!')

            def get_photo():
                """Метод возвращает url c картинкой максимального размера."""
                compair = []
                try:
                    for item in items[0]['sizes']:
                        compair.append(item['height'])
                    for d in items[0]['sizes']:
                        if d['height'] == max(compair):
                            # Передает размер для записи в json
                            global size
                            size = d['type']
                            return d['url']
                except IndexError:
                    print('Такого размера нет!')

            def get_likes():
                """Возвращает количество лайков."""
                try:
                    return items[0]['likes']['count']
                except IndexError:
                    print('Информации о лайках нет!')

            def get_date():
                """Возвращает дату создания аватара"""
                return items[0]['date']

            def upload_on_disk():
                """Загружает фото на яндекс диск"""
                yandex_disk.get_list_files()
                yandex_disk.upload(fold_name, get_likes(), get_date(),
                                   get_photo(), size=size)
            upload_on_disk()


if __name__ == '__main__':
    access_token = TOKEN
    user_id = {'user1': '383701493', 'user2': '383650133', 'user3': '383575589',
               'user4': '383761693', 'user5': '383655896'}
    vk = VK(access_token, user_id)
    print(vk.get_user_photo())

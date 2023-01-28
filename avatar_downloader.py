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
                compair = []
                try:
                    for item in items[0]['sizes']:
                        compair.append(item['height'])
                    for d in items[0]['sizes']:
                        if d['height'] == max(compair):
                            link = d['url']
                            return link
                except IndexError:
                    print('Такого размера нет!')

            get_photo()

            def get_likes():
                try:
                    return items[0]['likes']['count']
                except IndexError:
                    print('Информации о лайках нет!')

            get_likes()

            def get_date():
                return items[0]['date']
            get_date()

            def upload_on_disk():
                """Загружает фото на яндекс диск"""
                yandex_disk.get_list_files()
                yandex_disk.upload(fold_name, get_likes(), get_date(), get_photo())
            upload_on_disk()

            # def write_download_log():
            #     with open()


if __name__ == '__main__':
    access_token = TOKEN
    user_id = {'user1': '383701493', 'user2': '383650133', 'user3': '383575893',
               'user4': '383761693', 'user5': '260609441'}
    vk = VK(access_token, user_id)
    print(vk.get_user_photo())

from pprint import pprint

import requests
from token_yandex import TOKEN
exited_files = []


class YaUploader:
    link_for_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    link_for_create_folder = 'https://cloud-api.yandex.net/v1/disk/resources'
    link_for_gets_list_files = 'https://cloud-api.yandex.net/v1/disk/resources/files'

    def __init__(self):
        self.token = token

    @property
    def headers(self):
        """Метод авторизует на диске"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def create_folder(self, folder_name: str):
        """Метод создает папку на диске"""
        params = {'path': folder_name}
        response = requests.put(self.link_for_create_folder, params=params,
                                headers=self.headers)
        if response.status_code == 201:
            print('Папка создана!')
        else:
            return 'Произошла ошибка папка не создана!', response.status_code

    def get_list_files(self):
        """Метод получает список файлов на яндекс диске"""
        response = requests.get(self.link_for_gets_list_files,
                                headers=self.headers)
        list_of_files = response.json()
        items = list_of_files['items']
        for item in items:
            item['name'].append(exited_files)
            return item['name']

    def upload(self, file_path: str, likes: str, url: str):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        file_name = f'{likes}.jpg'
        params = {'path': f'{file_path}/{file_name}', 'url': f'{url}'}
        response = requests.post(self.link_for_upload, params=params,
                                 headers=self.headers)
        if response.status_code == 202:
            print(f'Файл загружен в папку {file_path}')
        else:
            return 'Произошла ошибка!', response.status_code


token = TOKEN

import json
import requests
from token_yandex import TOKEN
existed_files = []


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
            existed_files.append(item['name'])

    def upload(self, file_path: str, likes: str, date: str, url: str, size):
        """Метод загружает файлы по списку existed list на яндекс диск"""
        file_name = f'{likes}.jpg'
        file_name_date = f'{likes}_{date}.jpg'

        def writing_json(file_name):
            """Метод записывает имя и размер аватарки в json"""
            # По непонятным мне причинам запись в json происходит криво.
            data_for_json = {
                "file_name": f"{file_name}",
                "size": f"{size}"
                }

            # Сериализация json
            json_object = json.dumps(data_for_json, indent=4)

            # Запись данных, а именно имя файла и размер в json
            with open("avatars.json", "a+") as outfile:
                outfile.write(json_object)
        # Надо бы заняться рефакторингом, но лень
        if file_name in existed_files:
            params = {'path': f'{file_path}/{file_name_date}', 'url': f'{url}'}
            response = requests.post(self.link_for_upload, params=params,
                                         headers=self.headers)
            if response.status_code == 202:
                writing_json(file_name_date)
                print(f'Файл {file_name_date} загружен в папку {file_path}')
            else:
                return 'Произошла ошибка!', response.status_code
        else:
            params = {'path': f'{file_path}/{file_name}',
                      'url': f'{url}'}
            response = requests.post(self.link_for_upload, params=params,
                                     headers=self.headers)
            if response.status_code == 202:
                writing_json(file_name)
                print(f'Файл {file_name} загружен в папку {file_path}')
            else:
                return 'Произошла ошибка!', response.status_code


token = TOKEN

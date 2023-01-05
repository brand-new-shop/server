import httpx


class TelegramBot:

    def __init__(self, token: str):
        self.__token = token

    @property
    def base_url(self):
        return f'https://api.telegram.org/bot{self.__token}'

    def send_message(self, chat_id: int, text: str) -> bool:
        url = self.base_url + '/sendMessage'
        response = httpx.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'html'})
        return response.json()['ok']

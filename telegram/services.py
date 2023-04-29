import httpx


class TelegramBot:

    def __init__(self, token: str):
        self.__token = token
        self.base_url = f'https://api.telegram.org/bot{self.__token}'

    def send_message(self, chat_id: int, text: str):
        url = f'{self.base_url}/sendMessage'
        request_data = {
            'chat_id': chat_id,
            'text': text,
        }
        print(httpx.post(url, json=request_data))

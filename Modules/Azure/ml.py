import requests


class EndPoints:
    API_KEY = '1Qzrzfw6xGP3wJUeVLqiDDHIyGgUsLQ9'

    @classmethod
    def request(cls, endpoints_url, data: dict):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + cls.API_KEY
        }
        response = requests.post(endpoints_url,
                                 headers=headers,
                                 json=data)

        if response.status_code == 200:
            print("예측 결과:", response.json())
        else:
            print("요청 실패:", response.status_code, response.text)

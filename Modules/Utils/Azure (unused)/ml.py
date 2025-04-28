import requests
# Azure
from azure.core.exceptions import ClientAuthenticationError
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential


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


class CLI:
    SUBSCRIPTION = "816b75c1-b4f0-4711-9630-754a975c67f0"
    RESOURCE_GROUP = "200759-rg"
    WS_NAME = "StockMarketAnalysis"

    @classmethod
    def ml_client(cls):
        # authenticate
        credential = DefaultAzureCredential()  # 환경 변수를 통한 사용자 인증
        try:
            credential.get_token("https://management.azure.com/.default")
        except ClientAuthenticationError as e:
            print("InteractiveBrowserCredential으로 대체됨")
            credential = InteractiveBrowserCredential()  # 로그인 프롬프트를 통한 사용자 인증

        # Get a handle to the workspace
        return MLClient(
            credential=credential,
            subscription_id=cls.SUBSCRIPTION,
            resource_group_name=cls.RESOURCE_GROUP,
            workspace_name=cls.WS_NAME,
        )

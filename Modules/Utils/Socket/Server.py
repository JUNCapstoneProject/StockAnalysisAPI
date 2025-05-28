import socket
import threading
import queue
import copy
import zlib
import json
# Bridge
from Modules.Utils.Socket.Interface import SocketInterface
from Modules.Utils.Socket.Scheduler import FCFS
from Modules.Utils.Socket.Web.Decorator import ROUTE_TABLE
from Modules.Utils.Socket.Messages.response import response_message
from API.Controller.Analysis.Finance import FinanceAnalysisController
from API.Controller.Analysis.News import NewsAnalysisController


class TCPSocketServer(SocketInterface):
    def __init__(self):
        self.message_queue = queue.Queue()
        FinanceAnalysisController()  # 등록
        NewsAnalysisController()  # 등록

    @staticmethod
    def handle_request(path, item: dict) -> dict:
        """
        item은 data를 갖고있는 딕셔너리
        """
        route = ROUTE_TABLE.get(path)
        print('ROUTE_TABLE', ROUTE_TABLE)
        if route:
            cls, method_name = route
            instance = cls()  # 클래스 인스턴스 생성
            method = getattr(instance, method_name)
            data = item['data']
            output = method(data)
            return output
        else:
            return {
                "status_code": 400,
                "message": "존재하지 않는 API 경로입니다"
            }

    def receive_client(self, client_socket):
        """
        메세지를 메세지 큐에 넣는 역할
        소켓이 수립되면 해당 스레드가 생성되며,
        연결이 종료되면 소켓을 종료하며 스레드 해제
        """
        while True:
            try:
                data = client_socket.recv(self.SOCKET_BYTE)
                if not data:  # 클라이언트 연결 종료
                    break

                message = zlib.decompress(data).decode('utf-8')
                print('put message')
                self.message_queue.put((message, client_socket))

            except ConnectionResetError:
                break
            except zlib.error as e:
                print(f"압축 해제 오류: {e}")
                break

        client_socket.close()

    def process_messages(self):
        """
        메세지 큐에서 메세지를 꺼내 처리하는 역할
        """
        while True:
            message, client_socket = FCFS(self.message_queue)
            message = json.loads(message)
            response = copy.deepcopy(response_message)  # 원본 메세지(딕셔너리)의 수정 방지

            request_url = message['header']['Request URL']
            path = request_url.split("/analysis")[1]
            item = message['body']['item']
            
            output = self.handle_request(path, item)
            # handle_request 과정에서 예외가 발생하면 pipeline_id가 없음
            response['response_id'] = output.get('pipeline_id', 'None')
            response['status_code'] = output['status_code']
            response['message'] = output.get('message', 'None')
            response['item'] = output.get('item', 'None')

            response = json.dumps(response)
            client_socket.sendall(response.encode())
            self.message_queue.task_done()

    def run(self):
        # 서버 소켓 설정
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.HOST, self.SERVER_PORT))
        server_socket.listen()

        # 메시지 처리 스레드 시작
        threading.Thread(target=self.process_messages, daemon=True).start()

        # 클라이언트 연결 수락
        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.receive_client, args=(client_socket,), daemon=True).start()

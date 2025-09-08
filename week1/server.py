# server.py (버그 수정 버전)
import socket
import threading

class ChatServer:
    """
    멀티쓰레드 기반의 TCP 채팅 서버 (데드락 문제 해결)
    """
    clients = []
    lock = threading.Lock()

    def __init__(self, host, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        print(f'[*] 서버가 {host}:{port}에서 시작되었습니다.')

    def broadcast(self, message):
        """
        서버에 접속된 모든 클라이언트에게 메시지를 전송합니다.
        Lock 점유 시간을 최소화하기 위해 클라이언트 목록의 복사본을 사용합니다.
        """
        # Lock을 걸어 현재 클라이언트 목록의 스냅샷(복사본)을 안전하게 생성
        with self.lock:
            # 복사본을 만들어 사용함으로써, 메시지를 보내는 동안 clients 리스트가 변경되어도 에러가 발생하지 않음
            current_clients = list(self.clients)

        # Lock을 해제한 상태에서 실제 메시지 전송 (I/O 작업은 오래 걸릴 수 있음)
        for client_data in current_clients:
            client_socket = client_data['socket']
            try:
                client_socket.send(message)
            except Exception as e:
                # 메시지 전송 실패 시 해당 클라이언트는 결국 자신의 쓰레드에서 처리되므로 여기서 제거하지 않음
                print(f'[!] 브로드캐스트 에러 ({client_data.get("nickname", "Unknown")}): {e}')

    def handle_client(self, client_socket, addr):
        """
        개별 클라이언트와의 통신을 쓰레드에서 처리합니다.
        """
        print(f'[*] {addr}에서 새로운 연결을 수락했습니다.')
        
        nickname = 'Unknown'  # 클라이언트가 닉네임을 보내기 전에 접속을 끊을 경우를 대비한 기본값
        try:
            nickname = client_socket.recv(1024).decode('utf-8')
            
            with self.lock:
                self.clients.append({'socket': client_socket, 'nickname': nickname})

            entry_message = f'[{nickname}] 님이 입장하셨습니다.'.encode('utf-8')
            print(entry_message.decode('utf-8'))
            self.broadcast(entry_message)
            
            while True:
                message = client_socket.recv(1024)
                if not message:  # 클라이언트가 비정상 종료하면 빈 메시지가 수신됨
                    break

                decoded_message = message.decode('utf-8')
                if decoded_message == '/종료':
                    break
                
                formatted_message = f'{nickname}> {decoded_message}'.encode('utf-8')
                self.broadcast(formatted_message)

        except ConnectionResetError:
            print(f'[!] {addr} ({nickname}) 와의 연결이 비정상적으로 끊어졌습니다.')
        except Exception as e:
            print(f'[!] {nickname} 클라이언트 처리 중 에러 발생: {e}')
        finally:
            # 어떤 이유로든 루프가 끝나면 클라이언트 제거 및 퇴장 알림 처리
            self.remove_client(client_socket, nickname)

    def remove_client(self, client_socket, nickname):
        """
        클라이언트 목록에서 특정 클라이언트를 제거하고, 퇴장 메시지를 브로드캐스트합니다.
        """
        # Lock을 사용하여 clients 리스트를 안전하게 수정
        with self.lock:
            client_to_remove = None
            for client in self.clients:
                if client['socket'] == client_socket:
                    client_to_remove = client
                    break
            
            if client_to_remove:
                self.clients.remove(client_to_remove)
                print(f'[*] {nickname} 님의 연결이 종료되어 목록에서 제거했습니다.')

        # << 여기가 핵심! >>
        # Lock을 해제한 후에 퇴장 메시지를 브로드캐스트하여 Deadlock을 방지합니다.
        exit_message = f'[{nickname}] 님이 퇴장하셨습니다.'.encode('utf-8')
        self.broadcast(exit_message)
        
        # 소켓 리소스 정리
        client_socket.close()

    def run_server(self):
        """
        무한 루프를 돌며 클라이언트의 접속을 기다리고, 각 접속마다 새 쓰레드를 생성합니다.
        """
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.daemon = True 
                thread.start()
        except KeyboardInterrupt:
            print('\n[*] 서버를 종료합니다.')
        finally:
            with self.lock:
                for client_data in self.clients:
                    client_data['socket'].close()
            self.server_socket.close()

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 9999
    
    server = ChatServer(HOST, PORT)
    server.run_server()
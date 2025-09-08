import socket
import threading

def receive_messages(client_socket):
    """
    서버로부터 메시지를 수신하여 출력하는 함수 (쓰레드에서 실행)
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except Exception:
            print('[!] 서버와의 연결이 끊어졌습니다.')
            break
    client_socket.close()

def send_messages(client_socket):
    """
    사용자 입력을 받아 서버로 메시지를 전송하는 함수 (쓰레드에서 실행)
    """
    while True:
        message = input()
        try:
            client_socket.send(message.encode('utf-8'))
            if message == '/종료':
                break
        except Exception:
            print('[!] 메시지 전송에 실패했습니다.')
            break
    client_socket.close()


def run_client(host, port):
    """
    클라이언트를 실행하는 메인 함수
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        print(f'[!] 서버 연결 실패: {e}')
        return

    # 서버 접속 후 닉네임 전송
    nickname = input('사용할 닉네임을 입력하세요: ')
    client_socket.send(nickname.encode('utf-8'))
    
    # 메시지 수신 쓰레드 시작
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # 메시지 발신 쓰레드 시작
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()
    
    # 발신 쓰레드가 종료될 때까지 (즉, '/종료'를 입력할 때까지) 대기
    send_thread.join()
    print('[*] 채팅을 종료합니다.')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 9999
    run_client(HOST, PORT)
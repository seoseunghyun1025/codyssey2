import http.server
import socketserver
from datetime import datetime

PORT = 8080

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    클라이언트의 GET 요청을 처리하는 핸들러 클래스
    """
    def do_GET(self):
        """
        GET 요청을 받았을 때 호출되는 메소드
        """
        # 접속 시간과 클라이언트 IP 주소 출력
        access_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        client_ip = self.client_address[0]
        print(f'접속 시간: {access_time}')
        print(f'클라이언트 IP: {client_ip}')
        print('---')

        try:
            # 200 OK 응답 헤더 전송
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # index.html 파일 읽기 및 전송
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, 'File Not Found: index.html')

def run_server():
    """
    지정된 포트에서 HTTP 서버를 실행하는 함수
    """
    handler_object = MyHttpRequestHandler
    with socketserver.TCPServer(('', PORT), handler_object) as httpd:
        print(f'서버가 {PORT} 포트에서 실행 중입니다...')
        print('중지하려면 Ctrl+C를 누르세요.')
        httpd.serve_forever()

if __name__ == '__main__':
    run_server()
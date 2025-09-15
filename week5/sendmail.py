# sendmail.py

import os
import smtplib
from email.message import EmailMessage

def send_gmail():
    """
    Gmail 계정을 사용하여 이메일을 발송합니다.
    환경 변수에서 계정 정보와 앱 비밀번호를 가져옵니다.
    """
    # 1. 환경 변수에서 정보 가져오기
    sender_email = os.getenv('GMAIL_ADDRESS')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not (sender_email and sender_password):
        print('오류: GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수를 설정해주세요.')
        return

    # 2. 메일 수신자 및 내용 설정
    # 여러 명에게 보내려면 리스트 형태로 입력: ['email1@example.com', 'email2@example.com']
    recipient_email = 'recipient@example.com'  # 받는 사람 이메일 주소를 여기에 입력하세요.
    
    subject = '파이썬으로 보내는 자동화 메일입니다.'
    body = '이 메일은 Python의 smtplib 라이브러리를 통해 자동으로 발송되었습니다.'

    # 3. 이메일 메시지 객체 생성
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)

    # 4. SMTP 서버에 연결 및 메일 발송
    try:
        # Gmail의 SMTP 서버 주소와 TLS 포트(587)
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        # SMTP 서버 연결
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # TLS 암호화 통신 시작
            server.starttls()
            
            # SMTP 서버에 로그인
            server.login(sender_email, sender_password)
            
            # 이메일 발송
            server.send_message(msg)
            
            print(f"성공: '{recipient_email}'(으)로 메일을 성공적으로 보냈습니다.")

    except smtplib.SMTPAuthenticationError:
        print('오류: SMTP 인증에 실패했습니다. 앱 비밀번호나 계정 설정을 확인하세요.')
    except smtplib.SMTPConnectError:
        print('오류: SMTP 서버에 연결할 수 없습니다. 주소나 포트를 확인하세요.')
    except Exception as e:
        print(f'메일 발송 중 알 수 없는 오류가 발생했습니다: {e}')

# --- 메인 실행 블록 ---
if __name__ == '__main__':
    send_gmail()
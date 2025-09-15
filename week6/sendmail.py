# sendmail.py (오류 수정 완료 버전)

import os
import csv
import smtplib
from email.message import EmailMessage

def read_targets_from_csv(filename):
    """CSV 파일에서 메일 수신자 목록을 읽어옵니다."""
    targets = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                targets.append({'name': row['이름'], 'email': row['이메일']})
    except FileNotFoundError:
        print(f"오류: '{filename}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"CSV 파일을 읽는 중 오류가 발생했습니다: {e}")
    return targets

def send_bulk_html_email(targets):
    """
    Gmail 계정을 사용하여 다수의 수신자에게 개인화된 HTML 이메일을 발송합니다.
    """
    sender_email = os.getenv('GMAIL_ADDRESS')
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not (sender_email and sender_password):
        print('오류: GMAIL_ADDRESS 또는 GMAIL_APP_PASSWORD 환경 변수를 설정해주세요.')
        return

    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            
            print(f"SMTP 서버에 로그인 성공. 총 {len(targets)}명에게 메일 발송을 시작합니다.")
            
            for index, target in enumerate(targets, 1):
                name = target['name']
                email = target['email']
                
                msg = EmailMessage()
                msg['Subject'] = f'{name}님, 화성에서 보내는 긴급 구조 요청입니다.'
                msg['From'] = sender_email
                msg['To'] = email
                
                # HTML 본문 내용 (완성된 버전)
                html_body = f"""
                <html>
                <body>
                    <h2 style="color: #c43131;">긴급 상황 보고 및 구조 요청</h2>
                    <p>안녕하세요, <strong>{name}</strong>님.</p>
                    <p>저는 화성 탐사선 '아레스-5'의 탐사대원 한송희 박사입니다.<br>
                    예상치 못한 사고로 조난되었으나, 현재 생존해 있으며 기지에서 이 메시지를 보내고 있습니다.</p>
                    <p>지구와의 교신이 성공한 지금, 여러분의 도움이 절실합니다.<br>
                    <strong>부디 이 메시지를 관련 기관에 전달하여 주시길 간곡히 부탁드립니다.</strong></p>
                    <p>생존을 위해 최선을 다하고 있겠습니다.</p>
                    <p>감사합니다.<br>
                    - 한송희 박사 드림</p>
                </body>
                </html>
                """
                
                # HTML 형식으로 메일 본문 추가
                msg.add_alternative(html_body, subtype='html')
                
                server.send_message(msg)
                print(f"({index}/{len(targets)}) '{name}'님에게 메일 발송 성공.")
                
            print("\n모든 메일을 성공적으로 발송했습니다.")

    except smtplib.SMTPAuthenticationError:
        print('오류: SMTP 인증에 실패했습니다. 앱 비밀번호나 계정 설정을 확인하세요.')
    except Exception as e:
        print(f'메일 발송 중 알 수 없는 오류가 발생했습니다: {e}')

# --- 메인 실행 블록 ---
if __name__ == '__main__':
    csv_filename = 'mail_target_list.csv'
    recipient_list = read_targets_from_csv(csv_filename)
    
    if recipient_list:
        send_bulk_html_email(recipient_list)
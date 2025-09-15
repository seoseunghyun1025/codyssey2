# crawling_Naver.py

import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- 함수 정의 ---
def get_naver_credentials():
    """
    환경 변수에서 네이버 아이디와 비밀번호를 가져옵니다.

    Returns:
        tuple: (아이디, 비밀번호) 튜플. 없으면 (None, None).
    """
    naver_id = os.getenv('NAVER_ID')
    naver_pw = os.getenv('NAVER_PW')
    return naver_id, naver_pw

def crawl_naver_unread_mail():
    """
    Selenium으로 네이버에 로그인하여 안 읽은 메일 수를 크롤링합니다.
    """
    naver_id, naver_pw = get_naver_credentials()

    if not (naver_id and naver_pw):
        print('오류: NAVER_ID 또는 NAVER_PW 환경 변수가 설정되지 않았습니다.')
        return []

    # WebDriver 설정
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    crawled_content = []

    try:
        # 1. 네이버 로그인 페이지로 이동
        driver.get('https://nid.naver.com/nidlogin.login')
        time.sleep(2)  # 페이지 로딩 대기

        # 2. 아이디 입력 (클립보드 사용)
        id_input = driver.find_element(By.ID, 'id')
        id_input.click()
        pyperclip.copy(naver_id)
        id_input.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 3. 비밀번호 입력 (클립보드 사용)
        pw_input = driver.find_element(By.ID, 'pw')
        pw_input.click()
        pyperclip.copy(naver_pw)
        pw_input.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)

        # 4. 로그인 버튼 클릭
        driver.find_element(By.ID, 'log.login').click()
        
        # --- !! 중요 !! ---
        # 로그인 시 보안문자, 2단계 인증 등이 나타날 수 있습니다.
        # 이 시간을 이용해 수동으로 인증을 완료해주세요.
        print('로그인 인증 대기 중... (15초)')
        time.sleep(15)

        # 5. 로그인 후 메일 정보 크롤링
        # 네이버 메인 페이지로 이동하여 메일 정보를 확인합니다.
        # (로그인 성공 시 자동으로 메인으로 갈 수도 있고, 아닐 수도 있기에 명시적 이동)
        driver.get('https://www.naver.com')
        time.sleep(3) # 페이지 로딩 대기
        
        # 메일 링크 영역의 전체 텍스트를 가져옴 (예: "메일 15")
        # 선택자는 네이버 페이지 구조 변경에 따라 달라질 수 있습니다.
        mail_element = driver.find_element(By.CSS_SELECTOR, 'a.nav.mail')
        
        mail_text = mail_element.text.replace('메일', '').strip()
        
        if mail_text.isdigit():
            content = f'읽지 않은 메일: {mail_text}개'
            crawled_content.append(content)
        else:
            # 숫자가 없는 경우 (안 읽은 메일이 0개)
            crawled_content.append('읽지 않은 메일: 0개')

    except Exception as e:
        print(f'크롤링 중 오류가 발생했습니다: {e}')
    
    finally:
        # 브라우저 종료
        driver.quit()
        
    return crawled_content

# --- 메인 실행 블록 ---
if __name__ == '__main__':
    mail_info = crawl_naver_unread_mail()
    
    print('\n--- 크롤링 결과 ---')
    if mail_info:
        print(mail_info)
    else:
        print('콘텐츠를 가져오는데 실패했습니다.')
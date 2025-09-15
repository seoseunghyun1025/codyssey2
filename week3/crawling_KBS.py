# crawling_KBS.py (수정된 최종 버전)

import requests
from bs4 import BeautifulSoup

def get_kbs_headline_news():
    """
    KBS 뉴스 웹사이트에 접속하여 주요 헤드라인 뉴스를 크롤링합니다.

    Returns:
        list: 헤드라인 뉴스 제목들이 담긴 리스트.
              크롤링에 실패하면 빈 리스트를 반환합니다.
    """
    url = 'https://news.kbs.co.kr'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    headline_list = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 요청이 실패하면 예외를 발생시킴

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ---!!! 여기가 수정된 부분입니다 !!!---
        # 변경된 웹사이트 구조에 맞춰 새로운 CSS 선택자로 교체
        # 'main-VOD-title' 클래스를 가진 div 태그 안의 텍스트를 찾습니다.
        news_items = soup.select('div.main-VOD-title')
        
        # 추가적으로 다른 영역의 주요 뉴스도 가져오기 (선택사항)
        # 'rank-news-title' 클래스를 가진 span 태그를 찾습니다.
        news_items.extend(soup.select('span.rank-news-title'))
        
        if not news_items:
            # 만약 위 선택자로도 뉴스를 찾지 못했다면, 이 메시지가 표시될 수 있습니다.
            print('알림: 지정된 선택자로 뉴스 아이템을 찾지 못했습니다. 웹사이트 구조가 변경되었을 수 있습니다.')

        for item in news_items:
            title = item.get_text(strip=True)
            if title:
                headline_list.append(title)

    except requests.exceptions.RequestException as e:
        print(f'Error: 요청 중 예외가 발생했습니다: {e}')
    
    return headline_list

if __name__ == '__main__':
    kbs_headlines = get_kbs_headline_news()
    
    if kbs_headlines:
        print('KBS 헤드라인 뉴스 목록:')
        for index, headline in enumerate(kbs_headlines, 1):
            print(f'{index}. {headline}')
    else:
        print('헤드라인 뉴스를 가져오는데 실패했습니다.')
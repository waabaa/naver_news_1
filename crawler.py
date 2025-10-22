"""
네이트 뉴스 크롤러 모듈
랭킹 뉴스를 크롤링하고 각 뉴스의 상세 내용을 가져옵니다.
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time


class NateNewsCrawler:
    def __init__(self):
        self.base_url = "https://news.nate.com"
        self.ranking_url = "https://news.nate.com/rank/interest?sc=all&p=day"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.nate.com/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Cache-Control': 'max-age=0'
        }

    def get_demo_news(self, limit: int = 10) -> List[Dict]:
        """
        데모용 샘플 뉴스를 반환합니다.
        """
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')

        demo_news = [
            {'rank': '1', 'title': '[데모] 어린 딸 지키려다…중학생들 탄 전동킥보드에 30대 치여 중태',
             'link': 'https://news.nate.com/view/20251022n02107', 'medium': 'SBS', 'date': today,
             'content': '중학생 2명이 타고 달리던 전동킥보드에 30대 여성이 치여 중태에 빠진 사실이 뒤늦게 알려졌습니다. 딸을 지키려다 사고를 당한 것으로 알려져 안타까움을 더하고 있습니다.'},
            {'rank': '2', 'title': '[데모] 이이경 사생활 폭로자, 돌연 사과 "AI 사진 장난…관심 받을 줄 몰랐다"',
             'link': 'https://news.nate.com/view/20251022n03756', 'medium': '스포츠조선', 'date': today,
             'content': '배우 이이경의 사생활을 폭로했던 A씨가 "악성 루머를 퍼트리게 돼서 정말 죄송하다. AI 사진을 썼다"면서 해당 루머가 사실이 아니라고 밝혔습니다.'},
            {'rank': '3', 'title': '[데모] 구속된 캄보디아 송환자, 한국인 110명 피눈물 쓰게 한 범죄조직',
             'link': 'https://news.nate.com/view/20251022n01171', 'medium': '한국일보', 'date': today,
             'content': '로맨스스캠부터 노쇼 사기 등 총 93억원을 뜯어낸 것으로 알려진 캄보디아 범죄조직이 검거됐습니다. 고액 알바로 유인한 뒤 감금, 폭행, 전기고문 등을 자행한 것으로 드러났습니다.'},
            {'rank': '4', 'title': '[데모] 박시은♥진태현 "왜 성인만 입양" 비난에 "내 가족 아닌가"',
             'link': 'https://news.nate.com/view/20251022n02825', 'medium': '뉴스엔', 'date': today,
             'content': '배우 진태현이 입양 비난에 대해 가족 사랑을 전했습니다. "진태현 박시은 부부로 인해 입양 문화가 더욱 확대되기를 바란다"고 밝혔습니다.'},
            {'rank': '5', 'title': '[데모] 금값, 12년 만에 최대 폭락…"랠리 끝났다" vs "일시 조정"',
             'link': 'https://news.nate.com/view/20251022n03197', 'medium': '한국경제', 'date': today,
             'content': '국제 금 가격이 사상 최고치를 찍은 지 하루 만에 6% 넘게 떨어지며 2013년 이후 최대 낙폭을 기록했습니다. 전문가들은 의견이 엇갈리고 있습니다.'},
            {'rank': '6', 'title': '[데모] "5만원만 보내고 안 갈래요"…사라지는 축의 의미',
             'link': 'https://news.nate.com/view/20251022n02480', 'medium': '쿠키뉴스', 'date': today,
             'content': '결혼식에 참석하지 않고 축의금만 보내는 사람들이 늘어나면서 축의의 의미가 퇴색되고 있다는 지적이 나왔습니다.'},
            {'rank': '7', 'title': '[데모] "적색수배 대상입니다"…알려주고 풀어준 한국 대사관',
             'link': 'https://news.nate.com/view/20251022n00807', 'medium': 'YTN', 'date': today,
             'content': '적색수배자임을 알면서도 석방시킨 한국 대사관 직원의 행태가 논란이 되고 있습니다.'},
            {'rank': '8', 'title': '[데모] "여보, 이 집에서 버티자" 갈아타기 미룬다…매수도, 매도도 스톱',
             'link': 'https://news.nate.com/view/20251022n01113', 'medium': '머니투데이', 'date': today,
             'content': '부동산 시장이 얼어붙으면서 집 갈아타기를 미루는 가구가 급증하고 있습니다.'},
            {'rank': '9', 'title': '[데모] 박수홍이 직접 응원한 임산부, 다섯째 출산 직후 뇌출혈…뇌사 판정 위기',
             'link': 'https://news.nate.com/view/20251022n00228', 'medium': '스포츠조선', 'date': today,
             'content': '박수홍이 응원했던 다둥이 임산부가 출산 직후 뇌출혈로 위중한 상태에 빠졌습니다.'},
            {'rank': '10', 'title': '[데모] 의원님들, F학점도 아깝습니다…존중·스타·정책 없는 3무 국감',
             'link': 'https://news.nate.com/view/20251022n01490', 'medium': '중앙일보', 'date': today,
             'content': '올해 국정감사가 존중도, 스타도, 정책도 없는 삼무(三無) 국감이라는 비판을 받고 있습니다.'},
        ]

        return demo_news[:limit]

    def get_ranking_news(self, limit: int = 10) -> List[Dict]:
        """
        네이트 랭킹뉴스 목록을 가져옵니다.

        Args:
            limit: 가져올 뉴스 개수 (기본값: 10)

        Returns:
            뉴스 목록 (제목, 링크, 순위 등 포함)
        """
        try:
            response = requests.get(self.ranking_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')
            news_list = []

            # 1-5위 뉴스 (mduSubjectList)
            subject_list = soup.select('div.mduSubjectList')
            for item in subject_list[:limit]:
                try:
                    rank_elem = item.select_one('dl.mduRank dt em')
                    title_elem = item.select_one('h2.tit')
                    link_elem = item.select_one('a.lt1')
                    medium_elem = item.select_one('span.medium')

                    if rank_elem and title_elem and link_elem:
                        rank = rank_elem.text.strip()
                        title = title_elem.text.strip()
                        link = link_elem['href']
                        medium = medium_elem.text.strip() if medium_elem else ""

                        # 링크가 상대경로인 경우 절대경로로 변환
                        if link.startswith('//'):
                            link = 'https:' + link
                        elif link.startswith('/'):
                            link = self.base_url + link

                        news_list.append({
                            'rank': rank,
                            'title': title,
                            'link': link,
                            'medium': medium
                        })
                except Exception as e:
                    print(f"개별 뉴스 파싱 오류: {e}")
                    continue

            # 6위 이후 뉴스 (mduSubject)
            if len(news_list) < limit:
                subject_items = soup.select('ul.mduSubject li')
                for item in subject_items:
                    if len(news_list) >= limit:
                        break

                    try:
                        rank_elem = item.select_one('dl.mduRank dt em')
                        title_elem = item.select_one('h2')
                        link_elem = item.select_one('a')
                        medium_elem = item.select_one('span.medium')

                        if rank_elem and title_elem and link_elem:
                            rank = rank_elem.text.strip()
                            title = title_elem.text.strip()
                            link = link_elem['href']
                            medium = medium_elem.text.strip() if medium_elem else ""

                            # 링크가 상대경로인 경우 절대경로로 변환
                            if link.startswith('//'):
                                link = 'https:' + link
                            elif link.startswith('/'):
                                link = self.base_url + link

                            news_list.append({
                                'rank': rank,
                                'title': title,
                                'link': link,
                                'medium': medium
                            })
                    except Exception as e:
                        print(f"개별 뉴스 파싱 오류: {e}")
                        continue

            return news_list[:limit]

        except Exception as e:
            print(f"랭킹 뉴스 크롤링 오류: {e}")
            print("데모 모드로 전환합니다...")
            return self.get_demo_news(limit)

    def get_news_content(self, url: str) -> Dict:
        """
        뉴스 상세 내용을 가져옵니다.

        Args:
            url: 뉴스 URL

        Returns:
            뉴스 상세 정보 (제목, 본문, 날짜 등)
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'html.parser')

            # 제목
            title_elem = soup.select_one('h1.articleTitle, h2.articleTitle, div.articleTitle')
            title = title_elem.text.strip() if title_elem else ""

            # 본문
            content_elem = soup.select_one('div#articleBody, div.articleBody, div#newsBody, div.newsBody')
            if content_elem:
                # 스크립트, 광고 등 제거
                for tag in content_elem.find_all(['script', 'style', 'iframe']):
                    tag.decompose()
                content = content_elem.get_text(separator='\n', strip=True)
            else:
                content = ""

            # 날짜
            date_elem = soup.select_one('span.articleDate, span.dateTime, div.articleDate')
            date = date_elem.text.strip() if date_elem else ""

            # 언론사
            medium_elem = soup.select_one('span.medium, div.medium, a.medium')
            medium = medium_elem.text.strip() if medium_elem else ""

            return {
                'title': title,
                'content': content,
                'date': date,
                'medium': medium,
                'url': url
            }

        except Exception as e:
            print(f"뉴스 내용 크롤링 오류: {e}")
            return {
                'title': "",
                'content': "",
                'date': "",
                'medium': "",
                'url': url
            }

    def crawl_top_news(self, count: int = 5) -> List[Dict]:
        """
        상위 랭킹 뉴스의 상세 내용까지 모두 가져옵니다.

        Args:
            count: 가져올 뉴스 개수

        Returns:
            뉴스 상세 정보 리스트
        """
        ranking_news = self.get_ranking_news(limit=count)
        detailed_news = []

        for news in ranking_news:
            # 데모 뉴스는 이미 content와 date를 포함
            if 'content' in news and 'date' in news:
                detailed_news.append({
                    'rank': news['rank'],
                    'title': news['title'],
                    'link': news['link'],
                    'medium': news['medium'],
                    'content': news['content'],
                    'date': news['date']
                })
            else:
                # 실제 크롤링이 필요한 경우
                print(f"크롤링 중: {news['rank']}위 - {news['title'][:30]}...")
                content = self.get_news_content(news['link'])

                detailed_news.append({
                    'rank': news['rank'],
                    'title': news['title'],
                    'link': news['link'],
                    'medium': news['medium'],
                    'content': content['content'],
                    'date': content['date']
                })

                # 서버 부하 방지를 위한 딜레이
                time.sleep(1)

        return detailed_news


if __name__ == "__main__":
    # 테스트 코드
    crawler = NateNewsCrawler()

    print("네이트 랭킹 뉴스 크롤링 테스트")
    print("=" * 50)

    news_list = crawler.get_ranking_news(limit=5)
    print(f"\n총 {len(news_list)}개의 뉴스를 찾았습니다.\n")

    for news in news_list:
        print(f"{news['rank']}위: {news['title']}")
        print(f"링크: {news['link']}")
        print(f"언론사: {news['medium']}")
        print("-" * 50)

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
        self.ranking_url = "https://news.nate.com/rank/?mid=n1000"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

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
            return []

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

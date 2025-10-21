"""
블로그 글 생성 모듈
크롤링한 뉴스를 바탕으로 새로운 블로그 글을 생성합니다.
"""

import os
from typing import List, Dict
import re


class BlogGenerator:
    def __init__(self, openai_api_key: str = None):
        """
        블로그 생성기 초기화

        Args:
            openai_api_key: OpenAI API 키 (선택사항)
        """
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        self.use_openai = bool(self.openai_api_key)

        if self.use_openai:
            try:
                import openai
                self.openai = openai
                self.openai.api_key = self.openai_api_key
            except ImportError:
                print("OpenAI 라이브러리가 설치되지 않았습니다. 템플릿 모드로 실행됩니다.")
                self.use_openai = False

    def generate_with_template(self, news_list: List[Dict]) -> str:
        """
        템플릿 기반으로 블로그 글을 생성합니다.

        Args:
            news_list: 뉴스 리스트

        Returns:
            생성된 블로그 글
        """
        if not news_list:
            return "뉴스 데이터가 없습니다."

        # 제목 생성
        today_date = news_list[0].get('date', '오늘')
        title = f"📰 {today_date} 네이트 핫이슈 뉴스 정리"

        # 인트로
        intro = f"""
안녕하세요! 오늘의 핫한 뉴스를 정리해드립니다.
네이트 랭킹뉴스에서 가장 많은 관심을 받고 있는 {len(news_list)}가지 소식을 선별했습니다.
"""

        # 본문 생성
        body_sections = []
        for i, news in enumerate(news_list, 1):
            rank = news.get('rank', i)
            news_title = news.get('title', '제목 없음')
            content = news.get('content', '')
            medium = news.get('medium', '')
            link = news.get('link', '')

            # 본문 요약 (처음 300자)
            summary = self._summarize_content(content, max_length=300)

            section = f"""
## {rank}위. {news_title}

{summary}

> 출처: {medium}
> 원문 링크: {link}
"""
            body_sections.append(section)

        # 마무리
        outro = """
---

오늘의 주요 뉴스를 정리해드렸습니다.
더 자세한 내용은 각 뉴스 링크를 통해 확인하실 수 있습니다.

매일 업데이트되는 새로운 소식으로 찾아뵙겠습니다! 😊
"""

        # 전체 글 조합
        blog_post = f"# {title}\n{intro}\n" + "\n".join(body_sections) + outro
        return blog_post

    def generate_with_ai(self, news_list: List[Dict], style: str = "informative") -> str:
        """
        AI를 사용하여 블로그 글을 생성합니다.

        Args:
            news_list: 뉴스 리스트
            style: 글 스타일 (informative, casual, professional)

        Returns:
            생성된 블로그 글
        """
        if not self.use_openai:
            return self.generate_with_template(news_list)

        try:
            # 뉴스 요약 정보 생성
            news_summaries = []
            for news in news_list[:5]:  # 최대 5개만 사용
                summary = {
                    'rank': news.get('rank', ''),
                    'title': news.get('title', ''),
                    'content': news.get('content', '')[:500],  # 처음 500자만
                    'medium': news.get('medium', '')
                }
                news_summaries.append(summary)

            # AI 프롬프트 생성
            style_guide = {
                "informative": "정보전달에 충실한 객관적인 톤",
                "casual": "친근하고 편안한 대화체",
                "professional": "전문적이고 격식있는 톤"
            }

            prompt = f"""
다음은 네이트 랭킹뉴스에서 가져온 오늘의 주요 뉴스입니다.
이를 바탕으로 {style_guide.get(style, '정보전달적인')} 스타일의 블로그 글을 작성해주세요.

뉴스 목록:
{self._format_news_for_prompt(news_summaries)}

요구사항:
1. 매력적인 제목 작성
2. 각 뉴스를 요약하고 핵심 내용 전달
3. 독자의 관심을 끌 수 있도록 작성
4. 마크다운 형식 사용
5. 각 뉴스별로 섹션 구분
6. 전체 길이는 1000-1500자 정도

블로그 글:
"""

            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 전문 블로그 작가입니다. 뉴스를 재미있고 유익하게 재구성하는 능력이 뛰어납니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            blog_post = response.choices[0].message.content
            return blog_post

        except Exception as e:
            print(f"AI 생성 오류: {e}")
            print("템플릿 모드로 전환합니다.")
            return self.generate_with_template(news_list)

    def _summarize_content(self, content: str, max_length: int = 300) -> str:
        """
        뉴스 본문을 요약합니다.

        Args:
            content: 원본 내용
            max_length: 최대 길이

        Returns:
            요약된 내용
        """
        if not content:
            return "본문 내용이 없습니다."

        # 줄바꿈과 공백 정리
        content = re.sub(r'\s+', ' ', content).strip()

        # 최대 길이로 자르기
        if len(content) > max_length:
            content = content[:max_length] + "..."

        return content

    def _format_news_for_prompt(self, news_list: List[Dict]) -> str:
        """
        AI 프롬프트용으로 뉴스를 포맷팅합니다.
        """
        formatted = []
        for news in news_list:
            formatted.append(f"""
[{news['rank']}위] {news['title']}
출처: {news['medium']}
내용: {news['content']}
---
""")
        return "\n".join(formatted)

    def generate(self, news_list: List[Dict], mode: str = "template", style: str = "informative") -> str:
        """
        블로그 글을 생성합니다.

        Args:
            news_list: 뉴스 리스트
            mode: 생성 모드 ('template' 또는 'ai')
            style: 글 스타일 (mode가 'ai'일 때만 적용)

        Returns:
            생성된 블로그 글
        """
        if mode == "ai" and self.use_openai:
            return self.generate_with_ai(news_list, style)
        else:
            return self.generate_with_template(news_list)


if __name__ == "__main__":
    # 테스트 코드
    sample_news = [
        {
            'rank': '1',
            'title': '테스트 뉴스 제목',
            'content': '이것은 테스트 뉴스 내용입니다. ' * 10,
            'medium': '테스트 언론사',
            'link': 'https://example.com',
            'date': '2025-10-22'
        }
    ]

    generator = BlogGenerator()
    blog_post = generator.generate(sample_news, mode="template")
    print(blog_post)

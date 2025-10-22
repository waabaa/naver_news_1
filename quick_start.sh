#!/bin/bash

# 네이트 뉴스 블로그 생성기 빠른 시작 스크립트

echo "================================================"
echo "  📰 네이트 뉴스 블로그 생성기"
echo "================================================"
echo ""

# 1. 패키지 설치
echo "1️⃣  패키지 설치 중..."
pip install -q -r requirements.txt
if [ $? -eq 0 ]; then
    echo "   ✅ 패키지 설치 완료"
else
    echo "   ❌ 패키지 설치 실패"
    exit 1
fi
echo ""

# 2. 간단한 테스트
echo "2️⃣  시스템 테스트 중..."
python -c "
from crawler import NateNewsCrawler
from blog_generator import BlogGenerator

crawler = NateNewsCrawler()
news_list = crawler.get_ranking_news(limit=3)
print(f'   ✅ {len(news_list)}개 뉴스 크롤링 성공')

generator = BlogGenerator()
blog = generator.generate(news_list, mode='template')
print(f'   ✅ 블로그 글 생성 성공 ({len(blog)}자)')
"
echo ""

# 3. 서버 실행 안내
echo "3️⃣  서버 실행 방법:"
echo "   python app.py"
echo ""
echo "4️⃣  브라우저 접속:"
echo "   http://localhost:5000"
echo ""
echo "================================================"
echo "  준비 완료! 위 명령어로 서버를 실행하세요."
echo "================================================"

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
간단한 블로그 생성 스크립트
사용법: python generate_blog.py [뉴스개수]
"""

import sys
from crawler import NateNewsCrawler
from blog_generator import BlogGenerator

def main():
    # 뉴스 개수 입력받기
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    count = min(max(count, 3), 10)  # 3~10 사이로 제한

    print(f"\n{'='*60}")
    print(f"📰 네이트 뉴스 블로그 생성 (뉴스 {count}개)")
    print(f"{'='*60}\n")

    # 크롤링
    print("1️⃣  뉴스 크롤링 중...")
    crawler = NateNewsCrawler()
    news_list = crawler.crawl_top_news(count=count)
    print(f"   ✅ {len(news_list)}개 뉴스 수집 완료\n")

    # 블로그 생성
    print("2️⃣  블로그 글 생성 중...")
    generator = BlogGenerator()
    blog = generator.generate(news_list, mode='template')
    print(f"   ✅ {len(blog)}자 블로그 생성 완료\n")

    # 결과 출력
    print(f"{'='*60}")
    print(blog)
    print(f"{'='*60}\n")

    # 파일 저장
    filename = f"blog_{count}news.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(blog)
    print(f"💾 파일 저장: {filename}\n")

if __name__ == "__main__":
    main()

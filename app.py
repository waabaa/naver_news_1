"""
네이트 뉴스 블로그 생성기 웹 애플리케이션
Flask 기반 웹서비스
"""

from flask import Flask, render_template, request, jsonify
from crawler import NateNewsCrawler
from blog_generator import BlogGenerator
import os
import markdown

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# 전역 객체
crawler = NateNewsCrawler()
blog_generator = BlogGenerator()


@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')


@app.route('/api/get-ranking-news', methods=['GET'])
def get_ranking_news():
    """
    랭킹 뉴스 목록을 가져옵니다.
    Query Parameters:
        - limit: 가져올 뉴스 개수 (기본값: 10)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(limit, 50)  # 최대 50개로 제한

        news_list = crawler.get_ranking_news(limit=limit)

        return jsonify({
            'success': True,
            'count': len(news_list),
            'news': news_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/get-news-content', methods=['POST'])
def get_news_content():
    """
    특정 뉴스의 상세 내용을 가져옵니다.
    POST Body:
        - url: 뉴스 URL
    """
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({
                'success': False,
                'error': 'URL이 필요합니다.'
            }), 400

        content = crawler.get_news_content(url)

        return jsonify({
            'success': True,
            'content': content
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/crawl-top-news', methods=['GET'])
def crawl_top_news():
    """
    상위 랭킹 뉴스의 상세 내용을 모두 가져옵니다.
    Query Parameters:
        - count: 가져올 뉴스 개수 (기본값: 5)
    """
    try:
        count = request.args.get('count', 5, type=int)
        count = min(count, 10)  # 최대 10개로 제한

        detailed_news = crawler.crawl_top_news(count=count)

        return jsonify({
            'success': True,
            'count': len(detailed_news),
            'news': detailed_news
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/generate-blog', methods=['POST'])
def generate_blog():
    """
    블로그 글을 생성합니다.
    POST Body:
        - news_list: 뉴스 리스트
        - mode: 생성 모드 ('template' 또는 'ai')
        - style: 글 스타일 ('informative', 'casual', 'professional')
    """
    try:
        data = request.get_json()
        news_list = data.get('news_list', [])
        mode = data.get('mode', 'template')
        style = data.get('style', 'informative')

        if not news_list:
            return jsonify({
                'success': False,
                'error': '뉴스 데이터가 필요합니다.'
            }), 400

        blog_post = blog_generator.generate(news_list, mode=mode, style=style)

        # 마크다운을 HTML로 변환
        blog_html = markdown.markdown(blog_post, extensions=['extra', 'nl2br'])

        return jsonify({
            'success': True,
            'blog_markdown': blog_post,
            'blog_html': blog_html
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/auto-generate', methods=['GET'])
def auto_generate():
    """
    자동으로 뉴스를 크롤링하고 블로그 글을 생성합니다.
    Query Parameters:
        - count: 뉴스 개수 (기본값: 5)
        - mode: 생성 모드 (기본값: 'template')
        - style: 글 스타일 (기본값: 'informative')
    """
    try:
        count = request.args.get('count', 5, type=int)
        mode = request.args.get('mode', 'template')
        style = request.args.get('style', 'informative')

        count = min(count, 10)  # 최대 10개로 제한

        # 뉴스 크롤링
        detailed_news = crawler.crawl_top_news(count=count)

        if not detailed_news:
            return jsonify({
                'success': False,
                'error': '뉴스를 가져올 수 없습니다.'
            }), 500

        # 블로그 글 생성
        blog_post = blog_generator.generate(detailed_news, mode=mode, style=style)

        # 마크다운을 HTML로 변환
        blog_html = markdown.markdown(blog_post, extensions=['extra', 'nl2br'])

        return jsonify({
            'success': True,
            'news_count': len(detailed_news),
            'news': detailed_news,
            'blog_markdown': blog_post,
            'blog_html': blog_html
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """헬스 체크"""
    return jsonify({
        'status': 'ok',
        'service': 'Nate News Blog Generator'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# 🚀 사용 설명서

## 빠른 시작

### 방법 1: 자동 스크립트 실행

```bash
./quick_start.sh
```

위 스크립트가 자동으로:
- 필요한 패키지 설치
- 시스템 테스트
- 실행 방법 안내

### 방법 2: 수동 설정

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 서버 실행
python app.py

# 3. 브라우저에서 접속
# http://localhost:5000
```

## 웹 인터페이스 사용법

### 1. 메인 페이지 접속
브라우저에서 `http://localhost:5000` 접속

### 2. 설정 선택
- **뉴스 개수**: 생성할 블로그에 포함할 뉴스 개수 (3~10개)
- **생성 모드**:
  - `템플릿 모드`: 즉시 사용 가능 (추천)
  - `AI 모드`: OpenAI API 키 필요
- **글 스타일**:
  - `정보 전달형`: 객관적이고 사실 중심
  - `친근한 대화체`: 부드럽고 편안한 톤
  - `전문적인 톤`: 격식있는 전문가 스타일

### 3. 블로그 생성
- **뉴스 미리보기** 버튼: 크롤링될 뉴스만 확인
- **블로그 글 자동 생성** 버튼: 뉴스 크롤링 + 블로그 생성 일괄 처리

### 4. 결과 활용
생성된 블로그는 두 가지 형태로 제공됩니다:

#### 미리보기 탭
- HTML로 렌더링된 최종 결과물
- 실제 블로그에 게시될 모습 확인

#### 마크다운 탭
- 원본 마크다운 코드
- 수정 및 편집 가능
- 다른 플랫폼에 복사해서 사용

#### 활용 방법
- **📋 마크다운 복사**: 클립보드로 즉시 복사
- **💾 다운로드**: `.md` 파일로 저장

## 데모 모드란?

네이트 사이트가 봇 접근을 차단하면 자동으로 **데모 모드**로 전환됩니다.

### 데모 모드의 특징
- ✅ 실제 서비스와 동일한 기능
- ✅ 샘플 뉴스 데이터 사용
- ✅ 제목에 `[데모]` 표시
- ✅ 블로그 생성 기능 완전 동작

### 실제 크롤링이 작동하지 않을 때
```
랭킹 뉴스 크롤링 오류: 403 Client Error...
데모 모드로 전환합니다...
```
위 메시지가 나오면 데모 모드로 실행 중입니다.

## AI 모드 사용 (선택사항)

### 1. OpenAI API 키 발급
1. https://platform.openai.com 접속
2. API Keys 메뉴에서 새 키 생성
3. 키 복사

### 2. 환경 변수 설정

#### Linux/Mac
```bash
export OPENAI_API_KEY="sk-..."
```

#### Windows (CMD)
```cmd
set OPENAI_API_KEY=sk-...
```

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="sk-..."
```

### 3. 서버 재시작
```bash
python app.py
```

### 4. AI 모드 선택
웹 인터페이스에서 "생성 모드"를 "AI 모드"로 선택

## API 직접 사용하기

### Python에서 사용

```python
from crawler import NateNewsCrawler
from blog_generator import BlogGenerator

# 크롤러 초기화
crawler = NateNewsCrawler()

# 뉴스 크롤링
news_list = crawler.crawl_top_news(count=5)

# 블로그 생성
generator = BlogGenerator()
blog_post = generator.generate(news_list, mode='template')

print(blog_post)
```

### cURL로 API 호출

```bash
# 자동 생성
curl "http://localhost:5000/api/auto-generate?count=5&mode=template"

# 뉴스 목록만
curl "http://localhost:5000/api/get-ranking-news?limit=10"
```

## 문제 해결

### 서버가 시작되지 않을 때
```bash
# 포트가 이미 사용중인지 확인
lsof -i :5000

# 다른 포트로 실행
python -c "from app import app; app.run(port=8080)"
```

### 패키지 설치 오류
```bash
# pip 업그레이드
pip install --upgrade pip

# 개별 설치 시도
pip install Flask
pip install beautifulsoup4
pip install requests
```

### 크롤링이 계속 실패할 때
- 데모 모드로 자동 전환되므로 문제없이 사용 가능
- 실제 크롤링이 필요하면 VPN 또는 프록시 사용 고려

## 팁과 요령

### 1. 블로그 플랫폼별 활용

#### 티스토리
- 마크다운 에디터 모드 선택
- 생성된 마크다운 전체 복사/붙여넣기

#### 네이버 블로그
- HTML 모드로 전환
- 미리보기 탭의 내용을 복사

#### Notion
- 마크다운 import 기능 사용
- 다운로드한 .md 파일 업로드

#### Medium
- 마크다운 직접 붙여넣기 가능
- 이미지는 별도 업로드 필요

### 2. 커스터마이징

블로그 스타일을 변경하려면 `blog_generator.py`의 템플릿 수정:

```python
def generate_with_template(self, news_list):
    # 여기서 제목, 인트로, 아웃로 등 수정 가능
    title = f"📰 {today_date} 네이트 핫이슈 뉴스 정리"
    # ...
```

### 3. 자동화

정기적으로 블로그를 생성하려면:

```bash
# cron 작업 추가 (매일 오전 9시)
0 9 * * * cd /path/to/naver_news_1 && python -c "from crawler import NateNewsCrawler; from blog_generator import BlogGenerator; crawler = NateNewsCrawler(); news = crawler.crawl_top_news(5); generator = BlogGenerator(); blog = generator.generate(news); open('daily_blog.md', 'w').write(blog)"
```

## 지원 및 문의

문제가 발생하면:
1. GitHub Issues 확인
2. 새 이슈 등록
3. 로그 파일 첨부

즐거운 블로그 작성 되세요! 🎉

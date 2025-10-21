# 📰 네이트 뉴스 블로그 생성기

네이트(Nate) 랭킹뉴스를 자동으로 크롤링하고, 그 내용을 바탕으로 새로운 블로그 글을 생성하는 웹 서비스입니다.

## ✨ 주요 기능

- 🔍 **네이트 랭킹뉴스 크롤링**: 실시간 인기 뉴스 자동 수집
- 📝 **자동 블로그 글 생성**: 템플릿 기반 또는 AI 기반 블로그 글 작성
- 🎨 **다양한 글 스타일**: 정보 전달형, 친근한 대화체, 전문적인 톤 선택 가능
- 💾 **마크다운 다운로드**: 생성된 글을 마크다운 파일로 다운로드
- 📋 **원클릭 복사**: 마크다운 내용 클립보드 복사
- 👀 **실시간 미리보기**: HTML로 변환된 블로그 글 미리보기

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd naver_news_1
```

### 2. 가상환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행

```bash
python app.py
```

### 5. 브라우저에서 접속

```
http://localhost:5000
```

## 📁 프로젝트 구조

```
naver_news_1/
├── app.py                 # Flask 메인 애플리케이션
├── crawler.py             # 네이트 뉴스 크롤러
├── blog_generator.py      # 블로그 글 생성기
├── requirements.txt       # Python 패키지 의존성
├── README.md             # 프로젝트 문서
├── templates/
│   └── index.html        # 메인 페이지 템플릿
└── static/
    ├── css/
    │   └── style.css     # 스타일시트
    └── js/
        └── main.js       # JavaScript 로직
```

## 🎯 사용 방법

### 1. 기본 사용

1. **뉴스 개수 선택**: 크롤링할 뉴스 개수 선택 (3~10개)
2. **생성 모드 선택**:
   - **템플릿 모드**: 별도 설정 없이 바로 사용 가능
   - **AI 모드**: OpenAI API 키 필요 (환경변수 `OPENAI_API_KEY` 설정)
3. **글 스타일 선택**: 정보 전달형, 친근한 대화체, 전문적인 톤 중 선택
4. **블로그 글 자동 생성** 버튼 클릭

### 2. 뉴스 미리보기

생성 전에 어떤 뉴스가 크롤링되는지 확인하려면 **뉴스 미리보기** 버튼을 클릭하세요.

### 3. 결과 활용

- **미리보기 탭**: HTML로 렌더링된 블로그 글 확인
- **마크다운 탭**: 원본 마크다운 코드 확인 및 편집
- **마크다운 복사**: 클립보드로 내용 복사
- **다운로드**: `.md` 파일로 다운로드

## 🔧 API 엔드포인트

### GET `/api/get-ranking-news`

네이트 랭킹뉴스 목록을 가져옵니다.

**Query Parameters:**
- `limit` (int): 가져올 뉴스 개수 (기본값: 10, 최대: 50)

**Response:**
```json
{
  "success": true,
  "count": 5,
  "news": [
    {
      "rank": "1",
      "title": "뉴스 제목",
      "link": "https://...",
      "medium": "언론사명"
    }
  ]
}
```

### GET `/api/crawl-top-news`

상위 랭킹 뉴스의 상세 내용을 가져옵니다.

**Query Parameters:**
- `count` (int): 가져올 뉴스 개수 (기본값: 5, 최대: 10)

**Response:**
```json
{
  "success": true,
  "count": 5,
  "news": [
    {
      "rank": "1",
      "title": "뉴스 제목",
      "link": "https://...",
      "medium": "언론사명",
      "content": "뉴스 본문...",
      "date": "2025-10-22"
    }
  ]
}
```

### GET `/api/auto-generate`

뉴스 크롤링과 블로그 글 생성을 한 번에 수행합니다.

**Query Parameters:**
- `count` (int): 뉴스 개수 (기본값: 5, 최대: 10)
- `mode` (str): 생성 모드 ('template' 또는 'ai', 기본값: 'template')
- `style` (str): 글 스타일 ('informative', 'casual', 'professional', 기본값: 'informative')

**Response:**
```json
{
  "success": true,
  "news_count": 5,
  "news": [...],
  "blog_markdown": "# 블로그 제목\n...",
  "blog_html": "<h1>블로그 제목</h1>..."
}
```

### POST `/api/generate-blog`

뉴스 데이터를 받아 블로그 글을 생성합니다.

**Request Body:**
```json
{
  "news_list": [...],
  "mode": "template",
  "style": "informative"
}
```

## 🤖 AI 모드 사용하기

AI 모드를 사용하려면 OpenAI API 키가 필요합니다.

### 환경변수 설정

```bash
export OPENAI_API_KEY="your-api-key-here"
```

또는 `.env` 파일 생성:

```
OPENAI_API_KEY=your-api-key-here
```

## ⚠️ 주의사항

- 웹 크롤링은 네이트 뉴스의 이용 약관을 준수해야 합니다.
- 과도한 크롤링은 서버에 부담을 줄 수 있으므로 적절한 딜레이를 포함하고 있습니다.
- AI 모드 사용 시 OpenAI API 사용료가 발생할 수 있습니다.
- 크롤링된 뉴스의 저작권은 각 언론사에 있습니다.

## 🛠️ 기술 스택

- **Backend**: Flask (Python 3.8+)
- **Web Scraping**: BeautifulSoup4, Requests
- **AI**: OpenAI GPT-3.5 (선택사항)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Markdown**: Python-Markdown

## 📝 라이선스

MIT License

## 🤝 기여

이슈 제출 및 풀 리퀘스트를 환영합니다!

## 📧 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 등록해주세요.

// DOM 요소
const generateBtn = document.getElementById('generateBtn');
const previewNewsBtn = document.getElementById('previewNewsBtn');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const newsPreviewSection = document.getElementById('newsPreviewSection');
const newsList = document.getElementById('newsList');
const resultSection = document.getElementById('resultSection');
const blogPreview = document.getElementById('blogPreview');
const blogMarkdown = document.getElementById('blogMarkdown');
const copyMarkdownBtn = document.getElementById('copyMarkdownBtn');
const downloadBtn = document.getElementById('downloadBtn');

// 설정 요소
const newsCountSelect = document.getElementById('newsCount');
const generateModeSelect = document.getElementById('generateMode');
const writeStyleSelect = document.getElementById('writeStyle');

// 탭 전환
const tabButtons = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.dataset.tab;

        // 모든 탭 버튼 비활성화
        tabButtons.forEach(btn => btn.classList.remove('active'));
        // 모든 탭 패인 숨기기
        tabPanes.forEach(pane => pane.classList.remove('active'));

        // 클릭한 탭 활성화
        button.classList.add('active');
        document.getElementById(tabName + 'Tab').classList.add('active');
    });
});

// 에러 메시지 표시
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

// 로딩 표시
function showLoading() {
    loading.classList.remove('hidden');
    generateBtn.disabled = true;
    previewNewsBtn.disabled = true;
}

function hideLoading() {
    loading.classList.add('hidden');
    generateBtn.disabled = false;
    previewNewsBtn.disabled = false;
}

// 뉴스 미리보기 표시
function displayNewsPreview(newsData) {
    newsList.innerHTML = '';

    newsData.forEach(news => {
        const newsItem = document.createElement('div');
        newsItem.className = 'news-item';

        newsItem.innerHTML = `
            <div class="news-item-header">
                <div class="news-rank">${news.rank}</div>
                <div class="news-title">${news.title}</div>
            </div>
            <div class="news-meta">${news.medium}</div>
            <a href="${news.link}" class="news-link" target="_blank" rel="noopener noreferrer">
                ${news.link}
            </a>
        `;

        newsList.appendChild(newsItem);
    });

    newsPreviewSection.classList.remove('hidden');
}

// 블로그 결과 표시
function displayBlogResult(blogMarkdownText, blogHtmlText) {
    blogMarkdown.value = blogMarkdownText;
    blogPreview.innerHTML = blogHtmlText;
    resultSection.classList.remove('hidden');

    // 결과 섹션으로 스크롤
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 뉴스 미리보기 버튼
previewNewsBtn.addEventListener('click', async () => {
    const count = parseInt(newsCountSelect.value);

    showLoading();
    newsPreviewSection.classList.add('hidden');
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch(`/api/get-ranking-news?limit=${count}`);
        const data = await response.json();

        if (data.success) {
            displayNewsPreview(data.news);
        } else {
            showError(data.error || '뉴스를 가져오는데 실패했습니다.');
        }
    } catch (error) {
        showError('서버 오류가 발생했습니다: ' + error.message);
    } finally {
        hideLoading();
    }
});

// 블로그 글 자동 생성 버튼
generateBtn.addEventListener('click', async () => {
    const count = parseInt(newsCountSelect.value);
    const mode = generateModeSelect.value;
    const style = writeStyleSelect.value;

    showLoading();
    newsPreviewSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch(
            `/api/auto-generate?count=${count}&mode=${mode}&style=${style}`
        );
        const data = await response.json();

        if (data.success) {
            // 뉴스 미리보기 표시
            displayNewsPreview(data.news);

            // 블로그 결과 표시
            displayBlogResult(data.blog_markdown, data.blog_html);
        } else {
            showError(data.error || '블로그 글 생성에 실패했습니다.');
        }
    } catch (error) {
        showError('서버 오류가 발생했습니다: ' + error.message);
    } finally {
        hideLoading();
    }
});

// 마크다운 복사 버튼
copyMarkdownBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(blogMarkdown.value);

        // 버튼 텍스트 변경으로 피드백
        const originalText = copyMarkdownBtn.textContent;
        copyMarkdownBtn.textContent = '✅ 복사완료!';
        setTimeout(() => {
            copyMarkdownBtn.textContent = originalText;
        }, 2000);
    } catch (error) {
        showError('복사에 실패했습니다: ' + error.message);
    }
});

// 다운로드 버튼
downloadBtn.addEventListener('click', () => {
    const content = blogMarkdown.value;
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;

    // 파일명 생성 (현재 날짜 포함)
    const today = new Date().toISOString().split('T')[0];
    a.download = `nate-news-blog-${today}.md`;

    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', () => {
    console.log('네이트 뉴스 블로그 생성기가 준비되었습니다!');
});

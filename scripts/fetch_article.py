"""
文章解析脚本
从 URL 获取文章内容并提取结构化信息
"""
import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime


def fetch_article_content(url):
    """获取文章内容"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"获取文章失败: {e}")
        return None


def extract_article_info(html_content):
    """从 HTML 提取文章信息"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取标题
    title = soup.find('h1')
    if title:
        title = title.get_text().strip()
    else:
        title = soup.title.get_text().strip() if soup.title else "未知标题"

    # 提取正文（简单实现，可以根据不同网站优化）
    paragraphs = soup.find_all('p')
    content = '\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

    return {
        "title": title,
        "content": content
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: python fetch_article.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"正在获取文章: {url}")

    html_content = fetch_article_content(url)
    if not html_content:
        sys.exit(1)

    article_info = extract_article_info(html_content)

    # 输出 JSON 格式
    output = {
        "url": url,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": article_info["title"],
        "content": article_info["content"][:1000]  # 限制内容长度
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

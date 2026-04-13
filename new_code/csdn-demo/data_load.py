import requests
requests.packages.urllib3.disable_warnings()  # 关掉警告

from bs4 import BeautifulSoup
from markdownify import markdownify
import os
import time
import random

# ===================== 【改成你自己的信息】 =====================
CSDN_USERNAME = "RK_Dangerous"
SAVE_DIR = "data"
# =================================================================

# 随机 User-Agent 列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}  # 增强 headers 以模拟真实浏览器

def get_article_urls(username):
    urls = []
    page = 1
    while True:
        list_url = f"https://blog.csdn.net/{username}/article/list/{page}"
        resp = requests.get(list_url, headers=headers, verify=False)
        if resp.status_code != 200:  # 成功的状态码
            break
        soup = BeautifulSoup(resp.text, "html.parser")  # 将HTML文本解析成BeautifulSoup对象
        articles = soup.select(".article-item-box a")
        if not articles:
            break
        for a in articles:
            url = a.get("href")
            if url and "article/details" in url:
                urls.append(url)
        page += 1
        time.sleep(random.uniform(1, 3))  # 随机延迟 1-3 秒
    return urls

def save_article_md(url):
    max_retry = 5
    for attempt in range(1, max_retry + 1):
        headers["User-Agent"] = random.choice(user_agents)
        try:
            resp = requests.get(url, headers=headers, verify=False, timeout=10)
        except Exception as e:
            print(f"请求失败({attempt}/{max_retry})：{url}，错误：{e}")
            time.sleep(random.uniform(2, 5))
            continue
        soup = BeautifulSoup(resp.text, "html.parser")

        # 检查是否是验证页面
        title_tag = soup.find("title")
        title_text = title_tag.get_text() if title_tag else ""
        if ("验证" in title_text) or ("Security" in title_text):
            print(f"第{attempt}次检测到验证页面，等待重试：{url}")
            time.sleep(random.uniform(5, 10))
            continue

        # 标题
        title_elem = soup.find("h1", class_="title-article")
        if not title_elem:
            title_elem = soup.find("h1")
        if not title_elem:
            title_elem = soup.find("title")
        if not title_elem:
            print(f"警告：无法找到标题，跳过此文章 {url}")
            return
        title = title_elem.get_text(strip=True)

        # 内容
        content_elem = soup.find("div", id="article_content")
        if not content_elem:
            content_elem = soup.find("div", class_="article-content")
        if not content_elem:
            content_elem = soup.find("article")
        if not content_elem:
            content_elem = soup.find("div", class_="blog-content-box")  # CSDN 常见容器
        if not content_elem:
            content_elem = soup.find("div", class_="content")  # 通用内容容器
        if not content_elem:
            print(f"警告：无法找到文章内容 {url}")
            # 调试：打印页面标题和部分 HTML
            print(f"页面标题：{title_text if title_text else '无'}")
            print(f"页面前500字符：{soup.get_text()[:500]}")
            return
        content_html = content_elem.decode_contents()

        # 转 md
        content_md = markdownify(content_html).strip()

        # 保存
        os.makedirs(SAVE_DIR, exist_ok=True)
        filename = title.replace("/", "_").replace("\\", "_").replace(":", "_") + ".md"
        path = os.path.join(SAVE_DIR, filename)

        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(content_md)
        print(f"已保存：{filename}")
        return
    print(f"多次重试后仍为验证页面，跳过：{url}")

if __name__ == "__main__":
    urls = get_article_urls(CSDN_USERNAME)
    print(f"共找到 {len(urls)} 篇文章")
    # urls = urls[6:9]
    for url in urls:
        try:
            save_article_md(url)
            time.sleep(random.uniform(2, 5))  # 随机延迟 2-5 秒
        except Exception as e:
            print(f"失败：{url}，错误：{e}")
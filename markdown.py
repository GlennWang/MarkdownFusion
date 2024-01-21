import requests
import markdown2

def read_md_file(file_path):
    """讀取MD檔案"""
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
    return md_content

def convert_to_html(md_content):
    """使用GitHub Markdown API轉換為HTML"""
    api_url = 'https://api.github.com/markdown'
    data = {
        'text': md_content,
        'mode': 'gfm',
        'context': 'github/gollum'
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f"Markdown轉換為HTML時發生錯誤：{response.status_code}")
        return None

def save_html_file(html_content, output_path, template_path):
    """存儲HTML檔案，將HTML內容插入到template的<article>標籤中"""
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # 插入HTML內容到<article>標籤中
    final_html_content = template_content.replace('<article class="markdown-body"></article>', f'<article class="markdown-body">\n{html_content}\n</article>')

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(final_html_content)

if __name__ == "__main__":
    # 輸入MD檔案路徑和輸出HTML檔案路徑
    md_file_path = '網頁設計問題集.md'
    html_output_path = 'output.html'
    template_path = 'template.html'

    # 讀取MD檔案
    md_content = read_md_file(md_file_path)

    # 使用GitHub Markdown API轉換為HTML
    html_content = convert_to_html(md_content)

    if html_content:
        # 存儲HTML檔案，將HTML內容插入到<article>標籤中
        save_html_file(html_content, html_output_path, template_path)
        print(f"HTML檔案成功存儲於 {html_output_path}")
    else:
        print("無法完成HTML轉換及存儲。")

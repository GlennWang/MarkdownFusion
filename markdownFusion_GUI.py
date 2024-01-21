import requests
import markdown2
import tkinter as tk
from tkinter import filedialog
import os

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

def choose_file(entry_widget):
    """選擇MD檔案"""
    file_path = filedialog.askopenfilename(title="選擇MD檔案", filetypes=[("Markdown files", "*.md")], initialdir=os.path.join(os.getcwd(), 'markdown-post'))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, file_path)

def choose_template(entry_widget):
    """選擇模板檔案"""
    template_path = filedialog.askopenfilename(title="選擇模板檔案", filetypes=[("HTML files", "*.html")], initialdir=os.path.join(os.getcwd(), 'templates'))
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, template_path)

def convert_and_save():
    """轉換並儲存HTML檔案"""
    md_file_path = entry_md.get()
    template_path = entry_template.get()
    output_file_name = entry_output.get()
    
    md_content = read_md_file(md_file_path)
    html_content = convert_to_html(md_content)

    if html_content:
        output_path = os.path.join('output-post', f'{output_file_name}.html')
        save_html_file(html_content, output_path, template_path)
        result_label.config(text=f"HTML檔案成功存儲於 {output_path}", fg="green")
    else:
        result_label.config(text="無法完成HTML轉換及存儲。", fg="red")

# 建立主視窗
root = tk.Tk()
root.title("Markdown轉換器")

# 創建和放置各種元件
label_md = tk.Label(root, text="選擇MD檔案:")
label_md.grid(row=0, column=0, padx=5, pady=5)

entry_md = tk.Entry(root, width=50)
entry_md.grid(row=0, column=1, padx=5, pady=5)

button_browse_md = tk.Button(root, text="瀏覽", command=lambda: choose_file(entry_md))
button_browse_md.grid(row=0, column=2, padx=5, pady=5)

label_template = tk.Label(root, text="選擇模板:")
label_template.grid(row=1, column=0, padx=5, pady=5)

entry_template = tk.Entry(root, width=50)
entry_template.grid(row=1, column=1, padx=5, pady=5)

button_browse_template = tk.Button(root, text="瀏覽", command=lambda: choose_template(entry_template))
button_browse_template.grid(row=1, column=2, padx=5, pady=5)

label_output = tk.Label(root, text="輸出檔案名稱:")
label_output.grid(row=2, column=0, padx=5, pady=5)

entry_output = tk.Entry(root, width=50)
entry_output.grid(row=2, column=1, padx=5, pady=5)

button_convert = tk.Button(root, text="轉換並儲存", command=convert_and_save)
button_convert.grid(row=3, column=1, padx=5, pady=10)

result_label = tk.Label(root, text="", fg="black")
result_label.grid(row=4, column=0, columnspan=3, pady=5)

# 啟動主視窗
root.mainloop()

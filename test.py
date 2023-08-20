from exporter import notion2post

if __name__ == "__main__":
    file_base = "tmp"
    page_id = "31c9ded666f543c590876a08526a4d64"
    title = "NAS守卫战"
    categories = ["学习", "脚本", "测试"]
    tags = ["python", "scripts", "notion"]
    notion2post(page_id, categories=categories, tags=tags, title=title)
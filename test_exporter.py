from exporter import notion2post

if __name__ == "__main__":
    file_base = "tmp"
    page_id = "31c9ded666xxxxxxx8526a4d64" # the page id does not involving the page title
    title = "exporter-test"
    categories = ["scripts", "test"]
    tags = ["python", "scripts", "notion"]
    notion2post(page_id, categories=categories, tags=tags, title=title)
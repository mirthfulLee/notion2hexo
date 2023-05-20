import os
import sys
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter
import datetime
import json

config = json.load(open("config.json"))
os.environ["NOTION_TOKEN"] = config["notion_token"]


def get_notion_title(page_id:str):
    # get page title as post title
    native_client = Client(auth=os.environ["NOTION_TOKEN"])
    page_properties = native_client.pages.retrieve(page_id)
    page_title = page_properties["properties"]["title"]["title"][0]["plain_text"]
    return page_title


def info2yaml(page_info:dict):
    yaml_str = "---\n"
    yaml_str += "title: {}\n".format(page_info["title"])
    yaml_str += "date: {}\n".format(page_info["date"])
    
    # add categories
    yaml_str += "categories:\n- [{}".format(page_info["categories"][0])
    for i in range(1, len(page_info["categories"])):
        yaml_str += ", {}".format(page_info["categories"][i])
    yaml_str += "]\n"
    
    # add tags
    yaml_str += "tags:\n"
    for tag in page_info["tags"]:
        yaml_str += "- {}\n".format(tag)
        
    yaml_str += "---\n\n"
    return yaml_str


def notion2post(page_id:str, categories:list, tags:list, title:str=None):
    if not title:
        title = get_notion_title(page_id)
    page_info = {
        "title": title,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%H:%S"),
        "categories": categories,
        "tags": tags,
    }
    page_info["output_path"] = os.path.join(file_base, page_info["title"])

    # get origin content data
    content_exporter = MarkdownExporter(block_id=page_id, output_path=page_info["output_path"], 
                                        output_filename=page_info["title"],download=True, unzipped=True)
    content_exporter.export()
    
    # process content
    md_file = os.path.join(file_base, page_info["title"], page_info["title"]+".md")
    origin_md = info2yaml(page_info)
    with open(md_file, encoding="utf-8") as md_obj:
        origin_md += md_obj.read()
    
    # change <br/> to \n
    origin_md = origin_md.replace("<br/>\n", "\n")
    # delete useless \n
    origin_md = origin_md.replace("\n\n-", "\n-")
    origin_md = origin_md.replace("\n\n\n", "\n\n")
    
    with open(md_file, mode="w",encoding="utf-8") as md_obj:
        md_obj.write(origin_md)
        print("new post: {}".format(md_file))
    

if __name__ == "__main__":
    file_base = "tmp"
    page_id = "xxxxxxxx"
    categories = ["学习", "脚本", "测试"]
    tags = ["python", "scripts", "notion"]
    notion2post(page_id, categories=categories, tags=tags)
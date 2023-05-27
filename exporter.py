import os
import sys
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter
import datetime
import json
import shutil

config = json.load(open("config.json", "r"))
os.environ["NOTION_TOKEN"] = config["notion_token"]
file_base = config["hexo_post_dir"]


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


def remove_old_post(page_info: dict):
    history_file = "history.json"
    try:
        page_title_dict = json.load(open(history_file, "r"))
    except:
        page_title_dict = dict()
    if page_info["page_id"] in page_title_dict.keys():
        old_title = page_title_dict[page_info["page_id"]]
        # TODO: remove old post content
        shutil.rmtree(os.path.join(file_base, old_title))
        os.remove(os.path.join(file_base, old_title+".md"))
    
    page_title_dict[page_info["page_id"]] = page_info["title"]
    # TODO: update the history (page_id title map) file
    json.dump(page_title_dict, open(history_file, "w"), indent=2)
    


def notion2post(page_id:str, categories:list, tags:list, title:str=None):
    if not title:
        title = get_notion_title(page_id)
    page_info = {
        "page_id": page_id,
        "title": title,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%H:%S"),
        "categories": categories,
        "tags": tags,
    }
    page_info["output_path"] = os.path.join(file_base, page_info["title"])
    remove_old_post(page_info)

    # get origin content data
    content_exporter = MarkdownExporter(block_id=page_id, output_path=page_info["output_path"], 
                                        output_filename="origin",download=True, unzipped=True)
    content_exporter.export()
    
    # process content
    md_file = os.path.join(file_base, page_info["title"], "origin.md")
    origin_md = info2yaml(page_info)
    with open(md_file, encoding="utf-8") as md_obj:
        origin_md += md_obj.read()
    
    # change <br/> to \n
    origin_md = origin_md.replace("<br/>\n", "\n")
    # delete useless \n
    origin_md = origin_md.replace("\n\n-", "\n-")
    origin_md = origin_md.replace("\n\n\n", "\n\n")
    
    # change the md file path (file_base/xxx.md)
    md_file = os.path.join(file_base, page_info["title"]+".md")
    with open(md_file, mode="w",encoding="utf-8") as md_obj:
        md_obj.write(origin_md)
        print("new post: {}".format(md_file))
    

if __name__ == "__main__":
    file_base = "tmp"
    page_id = "31c9ded666f543c590876a08526a4d64"
    categories = ["学习", "脚本", "测试"]
    tags = ["python", "scripts", "notion"]
    notion2post(page_id, categories=categories, tags=tags)
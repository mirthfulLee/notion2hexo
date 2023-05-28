import os
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter
import datetime
import json
import shutil
import logging
import yaml
logging.basicConfig(filename="history.log", level=logging.INFO)
logger = logging.getLogger()

id_title_map_file = "id_title.json"
config_file = "config.json"

# read config file
try:
    config = json.load(open(config_file, "r"))
    os.environ["NOTION_TOKEN"] = config["notion_token"]
    file_base = config["hexo_post_dir"]
except:
    logger.error("config.json not found!")


def get_notion_title(page_id:str):
    # get page title as post title
    native_client = Client(auth=os.environ["NOTION_TOKEN"])
    page_properties = native_client.pages.retrieve(page_id)
    page_title = page_properties["properties"]["title"]["title"][0]["plain_text"]
    return page_title
    

def get_post_title_with_id(page_id: str):
    try:
        id_title_dict = json.load(open(id_title_map_file, "r"))
        if page_id in id_title_dict.keys():
            return id_title_dict[page_id]
    except:
        logger.critical("file 'id_title.json' not found!")
        return None


def remove_post_with_title(title: str):
    if os.path.exists(os.path.join(file_base, title)):
        logger.info("old post removed!")
        shutil.rmtree(os.path.join(file_base, title))
        os.remove(os.path.join(file_base, title+".md"))


def update_id_title_map(page_id: str, title: str):
    try:
        id_title_dict = json.load(open(id_title_map_file, "r"))
    except:
        id_title_dict = dict()
    id_title_dict[page_id] = title
    # update the history (page_id title map) file
    json.dump(id_title_dict, open(id_title_map_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def clean_id_title_record(page_id: str):
    try:
        id_title_dict = json.load(open(id_title_map_file, "r"))
    except:
        id_title_dict = dict()
    id_title_dict.pop(page_id, None)
    json.dump(id_title_dict, open(id_title_map_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def process_content(content: str):
    # change <br/> to \n
    content = content.replace("<br/>\n", "\n")
    # delete useless \n
    content = content.replace("\n\n-", "\n-")
    content = content.replace("\n\n\n", "\n\n")
    return content


def read_old_page_info(old_title: str):
    old_info_file = os.path.join(file_base, old_title, "info.yaml")
    with open(old_info_file, encoding="utf-8") as info_f:
        page_info = yaml.safe_load(info_f)
        return page_info
    

def notion2post(page_id:str, categories:list, tags:list, title:str=None):
    logger.info("attempt to add a new hexo post with page_id = {}".format(page_id))
    old_title = get_post_title_with_id(page_id)
    # TODO: read old page_info from yaml when old_title exists
    if old_title is not None:
        # update post info and content
        logger.info("the old post of {} exists.".format(page_id))
        page_info = read_old_page_info(old_title)
        logger.info("the old page info is {}".format(page_info))
        remove_post_with_title(page_info["title"])
        # update post info
        if title is not None: page_info["title"] = title
        if len(categories) > 0: page_info["categories"] = categories
        if len(tags) > 0: page_info["tags"] = tags
    else:
        # create a new post
        title = title or get_notion_title(page_id)
        page_info = {
            "page_id": page_id,
            "title": title,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%H:%S"),
            "categories": categories,
            "tags": tags,
        }
        logger.info("the page info is: {}".format(page_info))
    update_id_title_map(page_id, title)
    output_dir = os.path.join(file_base, page_info["title"])

    # get origin content data
    content_exporter = MarkdownExporter(block_id=page_id, output_path=output_dir, 
                                        output_filename="origin",download=True, unzipped=True)
    content_exporter.export()
    
    # save or update page info to file
    info_file = os.path.join(output_dir, "info.yaml")
    with open(info_file, "w", encoding="utf-8") as info_f:
        info_str = yaml.dump(page_info, allow_unicode=True)
        info_f.write(info_str)

    md_file = os.path.join(output_dir, "origin.md")
    origin_md = "---\n{}\n---\n".format(info_str)
    with open(md_file, encoding="utf-8") as md_f:
        origin_md += md_f.read()
    
    # change the md file path (file_base/xxx.md)
    md_file = os.path.join(file_base, page_info["title"]+".md")
    with open(md_file, mode="w",encoding="utf-8") as md_obj:
        # process content
        md_obj.write(process_content(origin_md))
        logger.info("new post: {}".format(md_file))


def remove_post_with_id(page_id: str):
    title = get_post_title_with_id(page_id)
    if title is None: return
    remove_post_with_title(title)
    clean_id_title_record(page_id)


if __name__ == "__main__":
    read_old_page_info("NAS守卫战")

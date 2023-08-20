import os
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter
import datetime
import json
import shutil
import logging
log_file = "history.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%a, %d %b %Y %H:%M:%S", filemode="a")
logger = logging.getLogger()
# output log to stream as well
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

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
    

def get_post_filename_with_id(page_id: str):
    try:
        id_title_dict = json.load(open(id_title_map_file, "r"))
        if page_id in id_title_dict.keys():
            return id_title_dict[page_id]
    except:
        logger.critical("file 'id_title.json' not found!")
        return None


def remove_post_with_filename(filename: str):
    if os.path.exists(os.path.join(file_base, filename)):
        logger.info("old post - {} removed!".format(filename))
        shutil.rmtree(os.path.join(file_base, filename))
        os.remove(os.path.join(file_base, filename+".md"))


def update_id_title_map(page_id: str, title: str):
    try:
        id_title_dict = json.load(open(id_title_map_file, "r"))
    except:
        id_title_dict = dict()
    id_title_dict[page_id] = title
    # update the history (page_id title map) file
    json.dump(id_title_dict, open(id_title_map_file, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def clean_id_filename_record(page_id: str):
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
    old_info_file = os.path.join(file_base, old_title, "info.json")
    with open(old_info_file, encoding="utf-8") as info_f:
        page_info = json.load(info_f)
        return page_info
    

def notion2post(page_id:str, categories:list, tags:list, title:str=None):
    logger.info("attempt to add a new hexo post with page_id = {}".format(page_id))
    old_filename = get_post_filename_with_id(page_id)
    # read old page_info from json when old_title exists
    if old_filename is not None:
        # update post info and content
        logger.info("the old post of {} exists.".format(page_id))
        page_info = read_old_page_info(old_filename)
        logger.info("the old page info is {}".format(page_info))
        remove_post_with_filename(old_filename)
        # update post info
        if title is not None: page_info["title"] = title
        if len(categories) > 0: page_info["categories"] = categories
        if len(tags) > 0: page_info["tags"] = tags
        page_info["updated"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%H:%S")
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
    
    # the title might includes '/' which could result to error
    # multiple page might have same title
    filename = "notion-{}-{}".format(title, page_id[:8])
    filename = filename.replace("/", "-").replace("\\", "-")
    # page_info["filename"] = filename
    output_dir = os.path.join(file_base, filename)

    # get origin content data
    content_exporter = MarkdownExporter(block_id=page_id, output_path=output_dir, 
                                        output_filename="origin",download=True, unzipped=True)
    content_exporter.export()
    
    # save or update page info to file
    info_file = os.path.join(output_dir, "info.json")
    with open(info_file, "w", encoding="utf-8") as info_f:
        info_str = json.dumps(page_info, ensure_ascii=False, indent=2)
        info_f.write(info_str)

    md_file = os.path.join(output_dir, "origin.md")
    origin_md = "{}\n;;;\n".format(info_str[1:-1])
    with open(md_file, encoding="utf-8") as md_f:
        origin_md += md_f.read()
    # remove origin markdown file, or there might be some error during post production
    os.remove(md_file)
    
    # change the md file path (file_base/xxx.md)
    md_file = os.path.join(file_base, filename+".md")
    with open(md_file, mode="w",encoding="utf-8") as md_obj:
        # process content
        md_obj.write(process_content(origin_md))
        logger.info("new post: {}".format(md_file))
    
    update_id_title_map(page_id, filename)


def remove_post_with_id(page_id: str):
    filename = get_post_filename_with_id(page_id)
    if filename is None: return
    remove_post_with_filename(filename)
    clean_id_filename_record(page_id)


def clean_log_file():
    f = open(log_file, "w")
    f.close()


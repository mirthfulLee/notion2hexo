import argparse
import exporter

parser = argparse.ArgumentParser()
parser.add_argument("--action", type=str, default="export", help="the target action, including export, update, remove")
parser.add_argument("--page_id", type=str, help="the uid of notion page")
parser.add_argument("--title", type=str, default=None, help="the title of the post")
parser.add_argument("--categories", nargs="*", type=str, default=[], help="the detailed category path of the post")
parser.add_argument("--tags", nargs="*", type=str, default=[], help="the tags of the post")
args = parser.parse_args()

exporter.notion2post(page_id=args.page_id, categories=args.categories, tags=args.tags, title=args.title)
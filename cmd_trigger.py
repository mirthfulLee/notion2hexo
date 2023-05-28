import argparse
import exporter

parser = argparse.ArgumentParser()
parser.add_argument("--action", type=str, default="export", help="the target action, including export, remove")
parser.add_argument("--page_id", type=str, help="the uid of notion page")
parser.add_argument("--title", type=str, default=None, help="the title of the post")
parser.add_argument("--categories", nargs="*", type=str, default=[], help="the detailed category path of the post")
parser.add_argument("--tags", nargs="*", type=str, default=[], help="the tags of the post")
args = parser.parse_args()

if args.action == "export":
    exporter.notion2post(page_id=args.page_id, categories=args.categories, tags=args.tags, title=args.title)
elif args.action == "remove":
    exporter.remove_post_with_id(page_id=args.page_id)
elif args.action == "clean":
    # clean log file:
    exporter.clean_log_file()

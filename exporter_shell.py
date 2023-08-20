import exporter

def export_new_page():
    # ask for pageid
    page_id = input("the id of notion page:")

    # ask for title
    print("\nthe title of notion page is:{}".format(exporter.get_notion_title(page_id)))
    title = input("input the title of exported post(use notion title with empty):")
    if title == "":
        title = None

    # ask for categories
    categories = []
    print("\ninput the top-down category of the post line by line")
    while True:
        cate = input("input the category(end with empty):")
        if cate != "":
            categories.append(cate)
        else:
            break

    # ask for tags
    tags = []
    print("\ninput the tags of the post line by line")
    while True:
        tag = input("input the tag(end with empty):")
        if tag != "":
            tags.append(tag)
        else:
            break

    exporter.notion2post(page_id=page_id, categories=categories, tags=tags, title=title)

def remove_post():
    # ask for page_id
    page_id = input("\nthe id of notion page corresponding to the post to be removed:")
    exporter.remove_post_with_id(page_id=page_id)


def clean_log():
    # ask for page_id
    exporter.clean_log_file()


if __name__ == "__main__":
    # ask for action
    print("the action supported:\n\t* e: export new page\n\t* r: remove old post\n\t* c: clean export history")

    while True:
        action = input("\nthe action you wanted:")
        if action == "e":
            export_new_page()
        elif action == "r":
            remove_post()
        elif action == "c":
            # clean log file:
            exporter.clean_log_file()
        elif action == "q":
            quit()
        else:
            print("please input correct option(e/r/c/q)")
            continue
        break

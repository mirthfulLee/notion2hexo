# notion2hexo
export simple notion page to hexo post with cmd line
1. export notion page to hexo post in local repo within cmd
2. push to github repo


# dependency
python > 3.7
notion_client
notion2md
pyyaml

# USAGE
add config.json in the same dir of exporter.py
## config.json
``` json
{
    "notion_token": "secret_xxxxxxx", // integration token create in https://www.notion.so/my-integrations
    "hexo_post_dir": "/home/user-xxx/hexo-blog/source/_posts",  // local hexo post dir path
}
use command line to export pages
```
## trige with python cmd line
``` shell
# export or update page to post
python cmd_trigger.py --page_id 31c9ded666f543c590876a08526a4d64 --title '被黑客吊打的经历' --categories '[杂谈, 经历]' --tags 'linux' 'security' 'attack'
# remove post with page id
python cmd_trigger.py --action remove --page_id 31c9ded666f543c590876a08526a4d64
```
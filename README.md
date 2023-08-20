# notion2hexo

export simple notion page to hexo post with cmdline

1. export notion page to hexo post in local repo within cmd
2. push to github repo

## USAGE

## simple config

1. add `export.py` and `notion2post.sh` to hexo-blog root(in the same dir as `_config.yml`)
2. choose python env and update the notion token in `notion2post.sh`
    * the env must install the required package by `pip install -r requirments.txt`
3. use the shell to export notion page `bash notion2post.sh`

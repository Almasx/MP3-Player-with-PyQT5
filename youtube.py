import re
import urllib.parse
import urllib.request

import requests


def searh_by_name(music_name):
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    link = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    return link


def check_video_link(link: str):
    r = requests.get(link)
    return "Video unavailable" not in r.text and link.startswith('https://www.youtube.com/watch?v=')

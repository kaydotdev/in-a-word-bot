import re
from lxml import html

re_clean_html_tags = re.compile(r"<.*?>")
re_match_http_url = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
re_file_format = re.compile(r"^.*\.(txt|TXT)$")
re_normalize_http_response = re.compile(r"[ \n\t\r]+")


def remove_html_tags(response: str):
    def __remove_all_by_xpath__(__tree__, __xpath__):
        for el in __tree__.xpath(__xpath__):
            el.getparent().remove(el)

    tree = html.fromstring(response)

    for xpath in ["//head", "//script", "//style"]:
        __remove_all_by_xpath__(tree, xpath)

    return re.sub(re_clean_html_tags, '', html.tostring(tree).decode('utf-8'))


def normalize_http_response(response: str):
    return re_normalize_http_response.sub(' ', response)

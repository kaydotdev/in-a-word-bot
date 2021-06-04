import re


re_clean_html_tags = re.compile(r"<.*?>")
re_match_http_url = re.compile(r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$")
re_file_format = re.compile(r"^.*\.(txt|TXT)$")


def remove_html_tags(response: str):
    return re.sub(re_clean_html_tags, '', response)

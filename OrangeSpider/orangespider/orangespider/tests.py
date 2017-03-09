# -*- coding: utf-8 -*-
import re
from utils import filter_tags, clean_html, replace_charentity

html = """
aaa<p>11111111111</p>sss
"""


if __name__ == '__main__':
    re_pp = re.compile('</p>', re.I)
    s = re_pp.sub('\n', html)
    print s
    print filter_tags(html)

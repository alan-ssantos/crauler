import re


patterns_replaces = [
    (r'<div(.*?)class=\"wp-video\">(.|\n)*<\/div><\/div>', ''),
    (r'(\s(style|class|id|role|aria-label|data-ri|cellpNadding|cellspacing|height|width|border|itemprop)=")(.*?")', ''),
    # (r'\s+(?=<*\<)', ''),
    # (r'(&#[0-9a-zA-z]*\;)', ''),
    # (r'<[^/>][^>]*><\/[^>]+>', ''),
    # (r'<[^>!(td|i)][^>]*><\/[^>]+>', ''),
    (r'<figure.*>', ''),
    (r'<\/figure>', ''),
    (r'\r?\n|\r|\t', ''),
    (r'</img>', ''),
    # (r'<h2>(.*?)</h2>', ''),
    # (r'<p><strong>', '<h2>'),
    # (r'<\/strong><\/p>', '</h2>'),
    # (r'<br\/><\/h2>', '</h2>'),
    # (r'<strong>', ''),
    # (r'<\/strong>', ''),
    # (r'<span\stitle(.*?\'>)', ''),
    # (r'<span[^>]*>', ''),
    (r'<table[^>]*>', '<table class="table">'),
    # (r'<\/span>', ''),
    (r'<(\/)?h1[^>]*>', '<\g<1>h2>'),
    (r'<a[^>]*>', '<span>'),
    (r'<\/a>', '</span>'),
    (r'<label[^>]*>', '<p>'),
    (r'<\/label>', '</p>'),
    (r'<br>', '</p><p>'),
    # (r'<a ', '<a target="_blank" rel="nofollow" '),
    (r'<p>&nbsp;</p>', ''),
    (r'<p> </p>', ''),
    (r'\u200b', ''),
    (r'<span></span>', ''),
]


def clear_tags(content: str):
    output = content
    for pattern, replace in patterns_replaces:
        output = re.sub(pattern, replace, output)

    return output

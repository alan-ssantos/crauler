import re
from typing import Union

from utils.file_handler import get_image
from utils.slug import slug


patterns_replaces = [
    (r"<div(.*?)class=\"wp-video\">(.|\n)*<\/div><\/div>", ""),
    (r"(\s(style|class|id|role|aria-label|data-ri|cellpNadding|cellspacing|height|width|border|itemprop)=\".*?\")", ""),
    # (r'\s+(?=<*\<)', ''),
    # (r'(&#[0-9a-zA-z]*\;)', ''),
    # (r'<[^/>][^>]*><\/[^>]+>', ''),
    # (r'<[^>!(td|i)][^>]*><\/[^>]+>', ''),
    (r"<figure[^>]*>", ""),
    (r"<\/figure>", ""),
    (r"\r?\n|\r|\t", ""),
    (r"</img>", ""),
    # (r'<h2>(.*?)</h2>', ''),
    # (r'<p><strong>', '<h2>'),F
    # (r'<\/strong><\/p>', '</h2>'),
    # (r'<br\/><\/h2>', '</h2>'),
    # (r'<strong>', ''),
    # (r'<\/strong>', ''),
    # (r'<span\stitle(.*?\'>)', ''),
    # (r'<span[^>]*>', ''),
    (r"<table[^>]*>", '<table class="table">'),
    # (r'<\/span>', ''),
    (r"<(\/)?h1[^>]*>", "<\g<1>h2>"),
    (r"<a[^>]*>", "<span>"),
    (r"<\/a>", "</span>"),
    (r"<label[^>]*>", "<p>"),
    (r"<\/label>", "</p>"),
    (r"<br>", "</p><p>"),
    # (r'<a ', '<a target="_blank" rel="nofollow" '),
    (r"<p>&nbsp;</p>", ""),
    (r"<p> </p>", ""),
    (r"\u200b", ""),
    (r"<span></span>", ""),
    (r"<form[^>]*>(.|\n)*</form>", ""),
    (r"<noscript>(.*?)</noscript>", ""),
    (r"(<\/?div>){1,}", ""),
    (r"<ul>", '<ul class="list">'),
    # Adicionados para o site Rep Relógios
    (r"<span><i aria-hidden=\"true\"></i></span>", ""),
    (r"<span><span>", ""),
    (r"<\/span><\/span>", ""),
    (r"&nbsp;", " "),
    (r"<span>Download(.*?)</span>", ""),
    (r"<li><span>", "<li>"),
    (r"<\/span><\/li>", "</li>"),
    (r"<p></p>", ""),
]


def clear_tags(content: str) -> str:
    output = content
    for pattern, replace in patterns_replaces:
        output = re.sub(pattern, replace, output)

    return output


def format_date(year: Union[str, int], month: Union[str, int], day: Union[str, int]) -> str:
    month_abbreviations = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]

    if type(month) is str:
        month = month_abbreviations.index((month if len(month) <= 3 else month[:3]).lower()) + 1
    month = ("0" if month < 10 else "") + str(month)

    return f"{year}-{month}-{day} 00:00:00"


def content_images(content, images, image_title, images_folder):
    local_images = []
    for image in images:
        local_images.append(get_image(image, slug(image_title), images_folder))

    original_images = re.findall("<img[^>]*>", content)
    print(f"{len(local_images)}/{len(original_images)} replaced images in content.")

    for i, image in enumerate(original_images):
        local_image = f'<img src="doutor/uploads/{local_images[i]}" alt="{image_title}" title="{image_title}">'
        content = content.replace(image, local_image)

    return content


def create_description(title: str, base_description: str) -> str:
    description = escape_quotes(title) + " - " + escape_quotes(base_description)
    return description[:145] + "... Saiba mais."


def escape_quotes(text: str) -> str:
    escaped_text = text.replace("'", "&#39;")
    # escaped_text = text.replace('"', "&#34;")

    return escaped_text


def split_pop_strip(text: str) -> str:
    return text.split(":").pop().strip()


def set_bold(text: str) -> str:
    text = text.split(":")
    return f'<p><span class="font-weight-bold">{text[0]}: </span>{text[1]}</p>'

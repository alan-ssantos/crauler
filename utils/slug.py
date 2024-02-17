import re
import unicodedata


def slug(text: str) -> str:
    replace_with_space = ["a", "á", "à", "ante", "até", "após", "de", "desde", "em", "entre", "com", "para", "por", "perante", "sem", "sob", "sobre", "na", "no", "e", "do", "da", "de", "(", ")", "'", '"', ".", ",", "/", "°", "º", "ª", "-", "*", "&", ";", "–", "?", "!", "#", "|", "“", "”", "$",]
    replace_without_space = ["  ", " ", ",", "--", "/", '"', "`", "´", "'", ".", ":", "º", "°", "(", ")", "*", "&", ";", "?", "!", "#", "ª", "|", "“", "”", "$",]

    # Substitui caracteres com espaços
    regex_syntax_with_space = re.compile(f'(\s+)({"|".join(map(re.escape, replace_with_space))})(\s+|$)')
    url = " ".join(text.split())
    url = regex_syntax_with_space.sub("-", url.lower())

    # Substitui caracteres sem espaços
    regex_syntax_without_space = re.compile(f'({"|".join(map(re.escape, replace_without_space))})')
    url = regex_syntax_without_space.sub("-", url.lower())
    url = " ".join(url.split("-"))
    url = "-".join(url.split())

    # Remove diacríticos (acentos, cedilhas, etc.)
    url = "".join(c for c in unicodedata.normalize("NFD", url) if unicodedata.category(c) != "Mn")

    # Remove espaços extras e retorna a URL final
    return "-".join(url.split())

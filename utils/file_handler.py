import random
import urllib.parse
import urllib.request
from datetime import datetime


def get_extension(url: str) -> str:
    extension = url.split(".").pop()

    if len(extension) > 4 or not extension:
        try:
            response = urllib.request.urlopen(url)
            content_type = response.headers.get("Content-Type")
            extension = content_type.split("/").pop()
        except:
            print("Não foi possível recuperar a extensão do arquivo.")
            extension = None

    return extension


def set_filename(prefix, slug, extension) -> str:
    today_timestamp = int(datetime.today().timestamp())
    random_int = random.randint(0, 1000)
    return f"{prefix}-{slug}-{today_timestamp}{random_int}.{extension}"


def set_filepath(user_id, folder, filename) -> str:
    todayYear = str(datetime.today().year)
    todayMonth = str(datetime.today().month)
    return f'{user_id}/{folder}/{todayYear}/{todayMonth if todayMonth > "9" else "0" + todayMonth}/{filename}'


def get_image(image_url: str, image_slug: str, save_folder: str, user_id: int, path_folder="produtos", is_cover=False) -> str:
    image_extension = get_extension(image_url)
    image_extension = "jpg" if image_extension == "jpeg" else image_extension

    image_filename = set_filename(("cover" if is_cover else "post"), image_slug, image_extension)
    try:
        urllib.request.urlretrieve(f"{image_url}", f"{save_folder}/{image_filename}")
        print("Image saved successfully")
        image_path = set_filepath(user_id, path_folder, image_filename)
    except:
        print("Unable to save image")
        image_path = set_filepath(user_id, path_folder, "default.png")
    return image_path


def get_file(file_url: str, file_slug: str, user_id: int, save_folder: str, path_folder="downloads") -> str:
    file_filename = set_filename("download", file_slug, get_extension(file_url))

    try:
        urllib.request.urlretrieve(f"{file_url}", f"{save_folder}/{file_filename}")
        print("File saved successfully")
        file_path = set_filepath(user_id, path_folder, file_filename)

    except:
        print("Unable to save file")
        file_path = ""
    return file_path

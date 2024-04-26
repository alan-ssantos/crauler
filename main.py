# original project by datCloud

from tqdm import tqdm
import time
import os
import json

from PyInquirer import prompt

from adapters.chrome_web_driver import ChromeWebDriver
from controllers.content_controller import *
from controllers.downloads_controller import get_downloads
from controllers.gallery_controller import get_gallery_images

from utils.slug import slug
from utils.file_handler import get_image
from utils.content_handler import clear_tags, create_description, escape_quotes

images_folder = f"crauler-result/imagens-{str(int(time.time()))}"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

downloads_folder = f"crauler-result/downloads-{str(int(time.time()))}"
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

current_dir = os.getcwd()
queriesOutput = open(os.path.join(current_dir, "crauler-result/queries.sql"), "w+", encoding="utf-8")

# Carrega o arquivo JSON
config_file_path = os.path.join(current_dir, "config.json")
try:
    with open(config_file_path, "r", encoding="utf-8") as config_file:
        config_json = json.load(config_file)
except FileNotFoundError:
    print(f"Arquivo '{config_file_path}' não encontrado.")
    exit(1)
except json.JSONDecodeError:
    print(f"Erro ao decodificar o arquivo JSON: '{config_file_path}'. Verifique se o arquivo está em formato válido.")
    exit(1)

config = config_json["config"]
selectors = config_json["selectors"]

links = config_json["links"]

base_description = config["base_description"]

user_id = config["user_id"]

page_category = config["page_category_name"]
category_id = config["category_id"]
categories = config["categories"]

product_id = config["product_id"]

download_category_id = config["download_category_id"]
current_download_id = config["current_download_id"]

chrome_driver = ChromeWebDriver()

questions = [{"type": "confirm", "name": "is_test", "message": "É um teste?", "default": True}]
answers = prompt(questions)

testing = answers.get("is_test")
if testing == True:
    links = links[:3]

for link in tqdm(links):
    url = link["url"]
    category_id = link["category_id"]
    print(url)
    
    try:
        chrome_driver.driver.get(url)
    except:
        print("Caiu a conexão")
        print("Tentando novamente em 3 segundos...")
        time.sleep(1)
        print("Tentando novamente em 2 segundos...")
        time.sleep(1)
        print("Tentando novamente em 1 segundos...")
        time.sleep(1)
        print("Acessando link")
        chrome_driver.driver.get(url)

    # ---- TÍTULO DO PRODUTO
    page_title = get_page_title(chrome_driver, selectors["page_title"])
    page_slug = slug(page_title)

    # ---- CAPA DO PRODUTO
    page_cover = get_page_cover(chrome_driver, selectors["page_cover"])
    page_cover_result = get_image(page_cover, page_slug, images_folder, user_id, page_category, True)

    # ---- PREÇO ANTIGO DO PRODUTO
    # old_price = get_old_price(chrome_driver, ".summary.entry-summary del .woocommerce-Price-amount.amount")

    # ---- NOVO PREÇO DO PRODUTO
    # new_price = get_price(chrome_driver, ".summary.entry-summary ins .woocommerce-Price-amount.amount")

    # ---- CATEGORIA DO PRODUTO
    # category = get_page_category(chrome_driver, categories, ".product_meta .posted_in a")

    # ---- DATA E HORÁRIO DA PUBLICAÇÃO DO PRODUTO
    publish_date = get_publish_date(chrome_driver, selectors["publish_date"])

    # --- CONTEÚDO DO PRODUTO
    page_content = get_page_content(chrome_driver, selectors["page_content"], page_title, images_folder)

    # ---- BREVE DESCRIÇÃO DO PRODUTO
    page_short_description = get_page_short_description(chrome_driver, selectors["page_short_description"])

    # ---- GALERIA DE IMAGENS
    gallery = get_gallery_images(
        chrome_driver, "", user_id, category_id, product_id, page_slug, page_cover, images_folder
    )

    # ---- DOWNLOADS
    downloads_result = get_downloads(
        chrome_driver,
        selectors["downloads"],
        user_id,
        current_download_id,
        download_category_id,
        downloads_folder,
        page_title,
        publish_date,
    )

    if downloads_result:
        current_download_id = downloads_result[1]

    queriesOutput.write(
        f"""
INSERT INTO `dr_produtos`(
  user_empresa,
  cat_parent,
  prod_name,
  prod_title,
  prod_cover,
  prod_description,
  prod_brevedescription,
  prod_content,
  prod_date,
  url_relation,
  prod_status
  )
VALUES (
  {user_id},
  {category_id},
  '{page_slug}',
  '{escape_quotes(page_title).title()}',
  '{page_cover_result}',
  '{create_description(page_title, base_description)}',
  '{escape_quotes(clear_tags(page_short_description))}',
  '{escape_quotes(clear_tags(page_content))}',
  '{publish_date}',
  '{downloads_result[2] if downloads_result else ""}',
  2
  );\n
"""
    )
    if gallery:
        queriesOutput.write(gallery)
    if downloads_result:
        queriesOutput.write(downloads_result[0])

chrome_driver.close()
queriesOutput.close()

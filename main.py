# original project by datCloud

from tqdm import tqdm
import time
import os
import inspect

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

currentDirectory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
urlFile = open(os.path.join(currentDirectory, "hrefs.txt"), "r")
linksToCrawl = []
for line in urlFile:
    if line.find("#") == -1:
        linksToCrawl.append(line.rstrip())

urlFile.close()

queriesOutput = open(os.path.join(currentDirectory, "crauler-result/queries.sql"), "w+", encoding="utf-8")

baseURL = ""
base_description = "Os rodízios Squadroni permitem movimentação suave de móveis, além de emprestar a beleza de seu design aos itens de mobiliário, mesmo quando estáticos..."
page = "produtos"

categoryId = 1
productId = 1

categories = []

download_category_id = 5
current_download_id = 1

chrome_driver = ChromeWebDriver()

for link in tqdm(linksToCrawl):
    print(link)

    try:
        chrome_driver.driver.get(link)
    except:
        print("Caiu a conexão")
        print("Tentando novamente em 3 segundos...")
        time.sleep(1)
        print("Tentando novamente em 2 segundos...")
        time.sleep(1)
        print("Tentando novamente em 1 segundos...")
        time.sleep(1)
        print("Acessando link")
        chrome_driver.driver.get(link)

    # ---- TÍTULO DO PRODUTO
    page_title = get_page_title(chrome_driver, "h1.entry-title")

    # ---- SLUG DA PÁGINA
    page_slug = slug(page_title)

    # ---- CAPA DO PRODUTO
    page_cover = get_page_cover(chrome_driver, ".project-slider img.preload-me")

    # ---- PREÇO ANTIGO DO PRODUTO
    # old_price = get_old_price(".summary.entry-summary del .woocommerce-Price-amount.amount")

    # ---- NOVO PREÇO DO PRODUTO
    # new_price = get_price(".summary.entry-summary ins .woocommerce-Price-amount.amount")

    # ---- CATEGORIA DO PRODUTO
    # category = get_page_category(categories, ".product_meta .posted_in a")

    # ---- DATA E HORÁRIO DA PUBLICAÇÃO DO PRODUTO
    publish_date = get_publish_date(chrome_driver, None)

    # --- CONTEÚDO DO PRODUTO
    page_content = get_page_content(chrome_driver, ".project-content > *", page_title, images_folder)

    # ---- BREVE DESCRIÇÃO DO PRODUTO
    page_short_description = get_page_short_description(chrome_driver, ".project-content > *")

    # ---- GALERIA DE IMAGENS
    gallery = get_gallery_images(chrome_driver, "", categoryId, productId, page_slug, page_cover, images_folder)

    # ---- DOWNLOADS
    downloads, last_download_id, download_list = get_downloads(
        chrome_driver,
        ".project-content a[href*='.pdf']",
        current_download_id,
        download_category_id,
        downloads_folder,
        page_title,
        publish_date,
    )
    current_download_id = last_download_id

    queriesOutput.write(
        f"""
INSERT INTO `dr_produtos`(
  user_empresa,
  cat_parent,
  prod_name,
  prod_title,
  prod_cover,
  prod_description,
  prod_content,
  prod_date,
  url_relation,
  prod_status
  )
VALUES (
  2,
  {categoryId},
  '{page_slug}',
  '{escape_quotes(page_title).title()}',
  '{get_image(page_cover, page_slug, images_folder, page, True)}',
  '{create_description(page_title, base_description)}',
  '{escape_quotes(clear_tags(page_content))}',
  '{publish_date}',
  '{download_list}',
  2
  );\n
"""
    )
    if gallery:
        queriesOutput.write(gallery)
    if downloads:
        queriesOutput.write(downloads)

chrome_driver.close()
queriesOutput.close()

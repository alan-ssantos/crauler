# original project by datCloud

import urllib.request
import urllib.parse
from tqdm import tqdm
import time
import os
import inspect

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from controllers.content_controller import *

from utils.slug import slug
from utils.file_handler import get_file, get_image
from utils.content_handler import clear_tags, create_description, escape_quotes

images_folder = f"crauler-result/imagens-{str(int(time.time()))}"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

downloads_folder = f"crauler-result/downloads-{str(int(time.time()))}"
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

opener = urllib.request.build_opener()
opener.addheaders = [
    (
        "User-agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    )
]
urllib.request.install_opener(opener)


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
download_id = 1
download_list = []


for link in tqdm(linksToCrawl):
    print(link)

    try:
        driver.get(link)
    except:
        print("Caiu a conexão")
        print("Tentando novamente em 3 segundos...")
        time.sleep(1)
        print("Tentando novamente em 2 segundos...")
        time.sleep(1)
        print("Tentando novamente em 1 segundos...")
        time.sleep(1)
        print("Acessando link")
        driver.get(link)

    # ---- TÍTULO DO PRODUTO
    page_title = get_page_title("h1.entry-title")

    # ---- SLUG DA PÁGINA
    page_slug = slug(page_title)

    # ---- CAPA DO PRODUTO
    page_cover = get_page_cover(".project-slider img.preload-me")

    # ---- PREÇO ANTIGO DO PRODUTO
    # old_price = get_old_price(".summary.entry-summary del .woocommerce-Price-amount.amount")

    # ---- NOVO PREÇO DO PRODUTO
    # new_price = get_price(".summary.entry-summary ins .woocommerce-Price-amount.amount")

    # ---- CATEGORIA DO PRODUTO
    # category = get_page_category(categories, ".product_meta .posted_in a")

    # ---- DATA E HORÁRIO DA PUBLICAÇÃO DO PRODUTO
    publish_date = get_publish_date()

    # --- CONTEÚDO DO PRODUTO
    page_content = get_page_content(".project-content > *", page_title, images_folder)

    # ---- BREVE DESCRIÇÃO DO PRODUTO
    page_short_description = get_page_short_description(".project-content > *")

    # ---- GALERIA DE IMAGENS
    # try:
    #     prodGallery = WebDriverWait(driver, 10).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sp-thumbs a")))
    #     prodGallery.pop(0)

    #     print(f"Images on gallery: {len(prodGallery)}")
    #     if len(prodGallery) == 0:
    #         imagesSrc = [page_cover]
    #     else:
    #         imagesSrc = []

    #     for image in prodGallery:
    #         imagesSrc.append(image.get_attribute("href").strip())

    #     if len(imagesSrc) > 0:
    #         for i in range(len(imagesSrc)):
    #             currentImage = GetLocalImage(imagesSrc[i], postTitle)
    #             if currentImage:
    #                 queriesOutput.write(f'''
    #               INSERT INTO app_gallery (
    #                 user_empresa,
    #                 cat_parent,
    #                 gallery_rel,
    #                 gallery_file)
    #               VALUES (2,
    #                 {categoryId},
    #                 {productId},
    #                 '{currentImage}');\n
    #               ''')
    # except Exception as e:
    #     print(f"Exception:\n{e}")
    #     print("No gallery found in product")

    # ---- DOWNLOADS
    try:
        files = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".project-content a[href*='.pdf']"))
        )
        filesLinks = []

        for file in files:
            filesLinks.append(file.get_attribute("href").strip())

        if len(filesLinks) > 0:
            for i in range(len(filesLinks)):
                currentFile = get_file(filesLinks[i], page_slug, downloads_folder)
                if currentFile:
                    download_id += 1
                    download_list.append(download_id)
                    queriesOutput.write(
                        f"""INSERT INTO `dr_downloads` (
                            `dow_id`,
                            `user_empresa`,
                            `cat_parent`,
                            `dow_name`,
                            `dow_title`,
                            `dow_description`,
                            `dow_file`,
                            `dow_date`,
                            `dow_status`
                          )
                            VALUES (
                            {download_id},
                            2,
                            {download_category_id},
                            '{slug('Catálogo: '+page_title)}',
                            '{'Catálogo: '+page_title}',
                            '{'Catálogo: '+page_title}',
                            '{currentFile}',
                            '{publish_date}',
                            2
                          );\n"""
                    )
    except Exception as e:
        print(f"Exception:\n{e}")
        print("Nenhum arquivo para download foi encontrado no produto.")

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
  '{','.join(map(str, download_list))}',
  2
  );\n
"""
    )
    download_list.clear()


driver.quit()
queriesOutput.close()

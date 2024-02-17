# original project by datCloud

import urllib.request
import urllib.parse
from tqdm import tqdm
import re
import time
import os
import inspect
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.slug import slug
from utils.get_file import get_file, get_image
from utils.html_handler import clear_tags

images_folder = f"crauler-result/imagens-{str(int(time.time()))}"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

downloads_folder = f"crauler-result/downloads-{str(int(time.time()))}"
if not os.path.exists(downloads_folder):
    os.makedirs(downloads_folder)

opener = urllib.request.build_opener()
opener.addheaders = [(
    "User-agent",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
)]
urllib.request.install_opener(opener)


def CreateDrescription(title):
    description = EscapeQuotes(title) + " - " + EscapeQuotes(baseDescription)
    return description[:145] + "... Saiba mais."


def EscapeQuotes(str):
    return str.replace("'", "&#39;")  # .replace('"', '&#34;')


def SplitPopStrip(str):
    return str.split(":").pop().strip()


# def formatDate(day, month, year):
#     22 de junho de 2018
#     monthList = ['jan','fev','mar','abr','maio','jun','jul','ago','set','out','nov','dez']
#     month = monthList.index(month) + 1
#     month = ('0' if month < 10 else '') + str(month)
#     return f'{year}-{month}-{day} 00:00:00'


def formatDate(date):
    monthList = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                 "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",]
    day = date[0]
    # month = monthList.index(date[1].lower()) + 1
    # month = ('0' if month < 10 else '') + str(month)
    month = date[1]
    year = date[2]
    return f"{year}-{month}-{day} 00:00:00"


def SetBold(value):
    value = value.split(":")
    return f'<p><span class="font-weight-bold">{value[0]}: </span>{value[1]}</p>'


def ContentToLocal(content, images, title):
    contentImagesSrc = []
    for image in images:
        contentImagesSrc.append(get_image(image, slug(title), images_folder))
        # try:
        #     contentImagesSrc.append(GetLocalImage(image, title, folder = 'produto'))
        # except:
        #     contentImagesSrc.append(GetLocalImage(image.attrs['srcset'].split(" ")[0], title, folder = 'produto'))

    content = re.sub("<noscript>(.*?)</noscript>", "", content)
    originalImages = re.findall("<img[^\>]+>", content)

    print("Original - " + str(len(originalImages)))
    print("Images - " + str(len(images)))
    for i, image in enumerate(originalImages):
        content = content.replace(
            image, f'<img src="doutor/uploads/{contentImagesSrc[i]} title="{title}" alt="{title}">')

    return content


currentDirectory = os.path.dirname(
    os.path.abspath(inspect.getfile(inspect.currentframe())))
urlFile = open(os.path.join(currentDirectory, "hrefs.txt"), "r")
linksToCrawl = []
for line in urlFile:
    if (line.find('#') == -1):
        linksToCrawl.append(line.rstrip())

urlFile.close()

queriesOutput = open(os.path.join(
    currentDirectory, "crauler-result/queries.sql"), "w+", encoding="utf-8")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(), options=chrome_options)

# driver.set_window_position(0, 0)
# driver.maximize_window()

baseURL = ""
baseDescription = "Os rodízios Squadroni permitem movimentação suave de móveis, além de emprestar a beleza de seu design aos itens de mobiliário, mesmo quando estáticos..."
page = "produtos"
categoryId = 1
productId = 1
# categories = []
downloadCat = 5
download_id = 1
download_list = []


def encontrar_indice(entrada, alvo):
    for i, elemento in enumerate(entrada):
        if elemento == alvo:
            return i + 2
    return -1


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

    # ---- CAPA DO PRODUTO
    try:
        postImage = (WebDriverWait(driver, 30).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".project-slider img.preload-me"))).get_attribute("src").strip())

        postImage = re.sub(r"\?.*", "", postImage)
        print(postImage)
    except:
        postImage = "https://producao.mpitemporario.com.br/sig_site_base_full_beta/doutor/images/default.png"
        print("Cover not found")

    # ---- TÍTULO DO PRODUTO
    try:
        postTitle = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.entry-title"))).get_attribute("innerText").strip()
    except:
        print("Title not found")

    # ---- PREÇO ANTIGO DO PRODUTO
    # try:
    #     oldPrice = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".summary.entry-summary del .woocommerce-Price-amount.amount"))).get_attribute('innerText').strip()
    #     oldPrice = str.replace(oldPrice, "R$ ", "")
    #     oldPrice = float(str.replace(oldPrice, ",", "."))
    # except:
    #     print('Old Price not found')

    # ---- NOVO PREÇO DO PRODUTO
    # try:
    #     newPrice = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".summary.entry-summary ins .woocommerce-Price-amount.amount"))).get_attribute('innerText').strip()
    #     newPrice = str.replace(newPrice, "R$ ", "")
    #     newPrice = float(str.replace(newPrice, ",", "."))
    # except:
    #     print('Old Price not found')

    # ---- CATEGORIA DO PRODUTO
    # try:
    #     categ = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, ".product_meta .posted_in a"))).get_attribute('innerText').strip()

    #     categoryId = categories.index(categ) + 2

    #     print("categoria: " + categ)
    # except:
    #     print('Category not found')

    # ---- DATA E HORÁRIO DA PUBLICAÇÃO DO PRODUTO
    try:
        now = datetime.now()
        postDate = now.strftime("%Y-%m-%d %H:%M:%S")
        # postDate = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        #     (By.CSS_SELECTOR, ".date-info > .date"))).get_attribute('innerText').strip().split('/')
        # postDate = f'{postDate[2]}-{postDate[1]}-{postDate[0]} 00:00:00'
    except:
        print("Date not found")

    # --- CONTEÚDO DO PRODUTO
    try:
        postContent = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".project-content > *")))

        postContentArray = []
        for descElements in postContent:
            postContentArray.append(descElements.get_attribute("outerHTML"))

        postContent = "".join(postContentArray)
    except:
        print("Content not found")

    # ---- IMAGENS DENTRO DO CONTEÚDO DO PRODUTO
    postContentImages = False
    try:
        postContentImagesSelector = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".project-content img")))

        postContentImages = []
        for images in postContentImagesSelector:
            postContentImages.append(images.get_attribute("src"))
        # print(postContentImages)
    except:
        print("Images in content not found")

    postContentImages = (postContent if not postContentImages else ContentToLocal(
        postContent, postContentImages, postTitle))

    # ---- BREVE DESCRIÇÃO DO PRODUTO
    try:
        breveDescriptionContent = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "")))

        breveDescriptionContentArray = []
        for descElements in breveDescriptionContent:
            breveDescriptionContentArray.append(
                descElements.get_attribute("outerHTML"))

        breveContent = "".join(breveDescriptionContentArray)
    except:
        print("breveDescription not found")

    # ---- GALERIA DE IMAGENS
    # try:
    #     prodGallery = WebDriverWait(driver, 10).until(
    #         EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".sp-thumbs a")))
    #     prodGallery.pop(0)

    #     print(f"Images on gallery: {len(prodGallery)}")
    #     if len(prodGallery) == 0:
    #         imagesSrc = [postImage]
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
        files = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".project-content a[href*='.pdf']")))
        filesLinks = []

        for file in files:
            filesLinks.append(file.get_attribute("href").strip())

        if len(filesLinks) > 0:
            for i in range(len(filesLinks)):
                currentFile = get_file(
                    filesLinks[i], slug(postTitle), downloads_folder)
                if currentFile:
                    download_id += 1
                    download_list.append(download_id)
                    queriesOutput.write(
                        f'''INSERT INTO `dr_downloads` (
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
                            {downloadCat},
                            '{slug('Catálogo: '+postTitle)}',
                            '{'Catálogo: '+postTitle}',
                            '{'Catálogo: '+postTitle}',
                            '{currentFile}',
                            '{postDate}',
                            2
                          );\n''')
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
  '{slug(postTitle)}',
  '{EscapeQuotes(postTitle).title()}',
  '{get_image(postImage, slug(postTitle), images_folder, page, True)}',
  '{CreateDrescription(postTitle)}',
  '{EscapeQuotes(clear_tags(postContentImages))}',
  '{postDate}',
  '{','.join(map(str, download_list))}',
  2
  );\n
"""
    )
    download_list.clear()


driver.quit()
queriesOutput.close()

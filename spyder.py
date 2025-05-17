import nodriver
import asyncio
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import hashlib
from PIL import Image
import yaml
import sys

config = "config.yml"
CacheTXT = "cache.txt"

MIN_SIZE = 100  

def load_config():
    with open(config, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_cache():
    if not os.path.exists(CacheTXT):
        return set()
    with open(CacheTXT, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_cache(url):
    with open(CacheTXT, "a", encoding="utf-8") as f:
        f.write(url + "\n")

def load_url_netx(urls_executadas_ja):
    dados = load_config()
    urls_ja_feitas = load_cache()

    for bloco in dados:
        url = bloco.get("URL")

        if not url or url in urls_executadas_ja:
            continue
        if url in urls_ja_feitas:
            continue
        if url not in urls_ja_feitas:
            save_cache(url)

        return bloco

    return None

def gerar_slug_url(url):
    netloc = urlparse(url).netloc
    netloc = netloc.replace("www.", "")
    netloc = netloc.split(".")[0]
    return netloc.replace("_", "-").lower()

def generate_name_folder(url):
    slug = gerar_slug_url(url)
    hash_pequeno = hashlib.sha1(url.encode()).hexdigest()[:6]
    return f"{slug}-{hash_pequeno}"

async def process_url(link, namepast):
    browser = await nodriver.start(headless=True)
    page = await browser.get(link)
    await asyncio.sleep(5)
    
    nome = generate_name_folder(link)
    print("Salvando conteúdo em pasta:", nome)

    os.makedirs(f'{namepast}/{nome}/imagens', exist_ok=True)

    texto = await page.get_content()
    with open(f'{namepast}/{nome}/pagina.txt', 'w', encoding='utf-8') as f:
        f.write(texto)

    soup = BeautifulSoup(texto, 'html.parser')
    texto_limpo = soup.get_text(separator='\n', strip=True)
    with open(f'{namepast}/{nome}/pagina_limpa.txt', 'w', encoding='utf-8') as f:
        f.write(texto_limpo)

    img_tags = await page.query_selector_all("img")
    urls = []

    for m in img_tags:
        soup_img = BeautifulSoup(str(m), 'html.parser')
        img = soup_img.find('img')
        if img and img.has_attr('src'):
            src = img['src'].strip()
            if not src or src.lower().startswith('data:') or 'undefined' in src:
                continue

            try:
                width = int(img.get('width', 0))
            except:
                width = 0
            try:
                height = int(img.get('height', 0))
            except:
                height = 0

            if width >= MIN_SIZE and height >= MIN_SIZE:
                urls.append(src)
                print(f'Imagem grande encontrada: {src} ({width}x{height})')
            else:
                print(f'Imagem pequena ignorada: {src} ({width}x{height})')

    await page.close()

    for i, url in enumerate(urls, start=1):
        try:
            if not url.startswith("http"):
                url = f"https://{url.lstrip('/')}"
            response = requests.get(url)
            if response.status_code == 200:
                ext = os.path.splitext(urlparse(url).path)[1]
                if not ext or '.' not in ext:
                    ext = '.jpg'
                filename = f'{namepast}/{nome}/imagens/imagem_{i}{ext}'
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f'Salvou: {filename}')
            else:
                print(f'Erro ao baixar {url} (status {response.status_code})')
        except Exception as e:
            print(f'Erro ao baixar {url}: {e}')

    folden = os.path.join(os.getcwd(), f'{namepast}/{nome}/imagens')
    formats_suported = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")

    for arquivo_img in os.listdir(folden):
        if arquivo_img.lower().endswith(formats_suported):
            caminho = os.path.join(folden, arquivo_img)
            nome_base = os.path.splitext(caminho)[0]
            with Image.open(caminho) as imgg:
                imgg.save(f'{nome_base}.webp', format="WEBP")
                os.remove(caminho)

async def urls(url_base, filtro):

    browser = await nodriver.start(headless=True)
    page = await browser.get(url_base)

    await asyncio.sleep(5)

    html = await page.get_content()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    links = []
    for a in soup.find_all("a", href=True):
        href = a['href']
        if filtro in href:
            if href.startswith('/'):
                href = url_base + href
            elif not href.startswith('http'):
                href = url_base + '/' + href
            links.append(href)
    await page.close()
    return links

async def main():
    urls_executadas_ja = []

    if len(sys.argv) > 1:
        link = sys.argv[1]
        print(f"[MODO URL DIRETA] Escaneando: {link}")
        namepast = generate_name_folder(link)
        os.makedirs(f"{namepast}", exist_ok=True)
        await process_url(link, namepast)
        list_links = await urls(link, path)
        for url in list_links:
            await process_url(url, namepast)
        return

    while True:
        bloco = load_url_netx(urls_executadas_ja)
        if not bloco:
            print("Todas URLs processadas, encerrando.")
            break

        link = bloco["URL"]
        path = bloco["path"]
        namepast = generate_name_folder(link)
        os.makedirs(f"{namepast}", exist_ok=True)
        urls_executadas_ja.append(link)
        print("procurando pagínas aguarde...")
        list_links = await urls(link, path)
        for url in list_links:
            await process_url(url, namepast)

if __name__ == '__main__':
    asyncio.run(main())

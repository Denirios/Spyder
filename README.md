# 🕷️ Spyder – Crawler Inteligente com Navegador Real

Projeto desenvolvido por **Adenilton** ([@denirios](https://github.com/denirios)) como parte do portfólio pessoal.

**Spyder** é um crawler avançado feito em Python que utiliza um navegador real (headless) via [nodriver](https://github.com/nodriver/nodriver). Ele visita páginas, coleta imagens relevantes, extrai o texto da página e salva tudo em estrutura organizada no disco.

---

## 🚀 Funcionalidades

- Leitura de múltiplas URLs e filtros de caminhos (paths) a partir de um arquivo `config.yml`
- Modo automático: processa todas URLs do `config.yml` sequencialmente
- Modo direto: recebe URL como argumento e processa só ela e seus links filtrados
- Execução com navegador real (headless Chromium)
- Extração e download de imagens grandes (≥ 100x100 pixels)
- Conversão automática de imagens para `.webp`
- Salvamento de HTML bruto e texto limpo
- Sistema de cache (`cache.txt`) para evitar repetir URLs
- Organização automática em pastas nomeadas por domínio + hash

---

## 🛠 Tecnologias utilizadas

- Python 3.11+
- [nodriver](https://github.com/nodriver/nodriver)
- BeautifulSoup (bs4)
- requests
- Pillow (PIL)
- asyncio
- YAML

---

## 🧪 Como usar

### 1. Configure o arquivo `config.yml`

Defina as URLs que deseja visitar e os caminhos (paths) para filtrar os links a serem baixados:

```yaml
- URL: "https://example.com"
  path: "/produtos"

- URL: "https://filmesonline.com"
  path: "/filme"
```

O campo `path` atua como filtro: somente links que contiverem esse trecho serão baixados e processados.

---

### 2. Execute o Spyder no modo automático

```bash
python spyder.py
```

O script vai processar sequencialmente todas as URLs listadas no `config.yml`.

---

### 3. Execute no modo direto (URL única)

```bash
python spyder.py https://example.com
```

Neste modo, o Spyder processa apenas essa URL, e também baixa links encontrados nela que contenham o `path` definido no `config.yml` para essa URL.

---

## 📁 Estrutura dos arquivos salvos

```
example-a1b2c3/
├── pagina.txt            # HTML completo
├── pagina_limpa.txt      # Texto limpo (sem tags)
└── imagens/
    ├── imagem_1.webp
    └── imagem_2.webp
```

---

## 📄 Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ✍️ Autor

Desenvolvido com 💻 e dedicação por:

**Adenilton**  
[@denirios](https://github.com/denirios)

> “Crawler robusto, leve e configurável para as suas necessidades.”

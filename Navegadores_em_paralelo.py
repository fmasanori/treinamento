# Este script abre MAX_CONCURRENCY, no caso 3, browsers em paralelo, acessa uma url
# diferente de URLS em cada um deles, pega os linsk de cada página e printa na tela
#
## ATENÇÃO: Antes de rodar o script, inicialize o driver como um serviço ###
## mais informações em https://github.com/douglasdcm/caqui
#
# $ ./chromedriver --port=9999
#
## Em um outro terminal
#
# $ python Navagadores_em_paralelo.py
#
# saída >
# Link found '127' links in https://pypi.org/project/caqui/
# Link found '207' links in https://www.selenium.dev/documentation/
# Link found '611' links in https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal
# Link found '64' links in https://docs.python.org/3/library/asyncio.html
# Link found '189' links in https://github.com/DwarfThief/Raspagem-de-dados-para-iniciantes
# Link found '9695' links in https://www.w3.org/TR/webdriver/
# Link found '191' links in https://www.vagas.com.br/
# Link found '235' links in https://www.youtube.com/
# Link found '15' links in https://testautomationu.applitools.com/
# Link found '72' links in http://appium.io/docs/en/2.0/
# Link found '201' links in https://github.com/microsoft/WinAppDriver
# Link found '347' links in https://www.baixelivros.com.br/
# Link found '312' links in https://www.estantevirtual.com.br/
# Time: 18.40 sec

import asyncio
import time
from os import getcwd
from caqui.easy import AsyncDriver
from caqui.by import By

URLS = [
    "https://pypi.org/project/caqui/",
    "https://pt.wikipedia.org/wiki/Wikip%C3%A9dia:P%C3%A1gina_principal",
    "https://www.selenium.dev/documentation/",
    "https://www.w3.org/TR/webdriver/",
    "https://docs.python.org/3/library/asyncio.html",
    "https://github.com/DwarfThief/Raspagem-de-dados-para-iniciantes",
    "https://www.youtube.com/",
    "https://www.vagas.com.br/",
    "https://testautomationu.applitools.com/",
    "http://appium.io/docs/en/2.0/",
    "https://github.com/microsoft/WinAppDriver",
    "https://www.estantevirtual.com.br/",
    "https://www.baixelivros.com.br/",
]

BASE_DIR = getcwd()

MAX_CONCURRENCY = 3  # number of webdriver instances running
all_anchors = []
semaphore = asyncio.Semaphore(MAX_CONCURRENCY)


async def get_links(url):
    async with semaphore:
        remote = "http://127.0.0.1:9999"
        capabilities = {
            "desiredCapabilities": {
                "browserName": "chrome",
                "acceptInsecureCerts": True,
                "pageLoadStrategy": "eager",
                ## Descomente para rodar em headless mode
                # "goog:chromeOptions": {"extensions": [], "args": ["--headless"]},
            }
        }

        driver = AsyncDriver(remote, capabilities)

        await driver.get(url)
        links = await driver.find_elements(By.XPATH, "//a")

        print(f"Link found '{len(links)}' links in {url}")

        driver.quit()


async def main():
    tasks = [asyncio.ensure_future(get_links(url)) for url in URLS]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        end = time.time()
        print(f"Time: {end-start:.2f} sec")

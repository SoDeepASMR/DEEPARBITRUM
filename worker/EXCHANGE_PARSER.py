import time, pickle, datetime
import colorlabels as cl
import multiprocessing as mp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def NowTime():
    return f'{datetime.datetime.now().day}.' \
           f'{datetime.datetime.now().month}.' \
           f'{datetime.datetime.now().year} ' \
           f'{datetime.datetime.now().hour}:' \
           f'{datetime.datetime.now().minute}:' \
           f'{datetime.datetime.now().second}'


class parser:
    def __init__(self, links: dict):
        self.procs = []
        self.links = links

        self.parser = ExchangeParser()

    def worker(self):
        for ex, link in self.links.items():
            proc = mp.Process(target=self.parser.parse, args=(ex, link,))
            self.procs.append(proc)
            proc.start()

        for proc in self.procs:
            proc.join()

    @staticmethod
    def update_exchanges():
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # driver = webdriver.Chrome('./chromedriver', chrome_options=options)
        #
        # driver.get('https://coinmarketcap.com/en/rankings/exchanges/')
        #
        # driver.execute_script('window.scrollTo(0, 5000)')
        #
        # time.sleep(1)
        #
        # driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div[3]').click()

        links = {
            'Binance': 'https://coinmarketcap.com/en/exchanges/binance/?type=spot',
            'Bybit': 'https://coinmarketcap.com/en/exchanges/bybit/?type=spot',
            'KuCoin': 'https://coinmarketcap.com/en/exchanges/kucoin/?type=spot',
            'OKX': 'https://coinmarketcap.com/en/exchanges/okx/?type=spot',
            'Huobi Global': 'https://coinmarketcap.com/en/exchanges/huobi-global/?type=spot',
            'FTX': 'https://coinmarketcap.com/en/exchanges/ftx/?type=spot',
            'Gate.io': 'https://coinmarketcap.com/en/exchanges/gate-io/?type=spot',
            'EXMO': 'https://coinmarketcap.com/en/exchanges/exmo/?type=spot',
            'BitForex': 'https://coinmarketcap.com/en/exchanges/bitforex/?type=spot',
            'Bitfinex': 'https://coinmarketcap.com/en/exchanges/bitfinex/?type=spot',
            'Poloniex': 'https://coinmarketcap.com/en/exchanges/poloniex/?type=spot',
            'ProBit Global': 'https://coinmarketcap.com/en/exchanges/probit-exchange/?type=spot',
            'Coinbase Exchange': 'https://coinmarketcap.com/en/exchanges/coinbase-exchange/?type=spot',
            'Korbit': 'https://coinmarketcap.com/en/exchanges/korbit/?type=spot',
            'Upbit': 'https://coinmarketcap.com/en/exchanges/upbit/?type=spot',
            'Crypto.com Exchange': 'https://coinmarketcap.com/en/exchanges/crypto-com-exchange/?type=spot',
            'PancakeSwap (V2)': 'https://coinmarketcap.com/en/exchanges/pancakeswap-v2/?type=spot',
            'Bitstamp': 'https://coinmarketcap.com/en/exchanges/bitstamp/?type=spot',
            'BKEX': 'https://coinmarketcap.com/en/exchanges/bkex/?type=spot',
            'Blockchain.com': 'https://coinmarketcap.com/en/exchanges/blockchain-com-exchange/?type=spot',
            'Curve Finance': 'https://coinmarketcap.com/en/exchanges/curve-finance/?type=spot',
            'KLAYswap': 'https://coinmarketcap.com/en/exchanges/klayswap/?type=spot',
            'SushiSwap': 'https://coinmarketcap.com/en/exchanges/sushiswap/?type=spot',
            'Sun.io': 'https://coinmarketcap.com/en/exchanges/justswap/?type=spot'
        }

        with open('exchanges', 'wb+') as file:
            pickle.dump(links, file)


class ExchangeParser:
    def __init__(self):
        # self.data = {'Pair': {'Price': None, 'Volume': None, 'Liq': None}}
        self.data = []

    def parse(self, exchange: str, link: str):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Chrome(
            './chromedriver',
            chrome_options=options,
            service_log_path=None,
            desired_capabilities=caps
        )

        flag = False
        count = 0
        while not self.data:
            driver.get(link)
            try:
                while True:
                    if count == 10:
                        flag = True
                        break

                    time.sleep(1)
                    button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[3]/div[3]/button')
                    webdriver.ActionChains(driver).scroll_to_element(button)
                    button.send_keys(Keys.PAGE_DOWN)
                    button.click()
                    count += 1

            except Exception:
                self.data = [_.text.split('\n') for _ in driver.find_elements(By.TAG_NAME, 'tr')[1:]]

            if flag:
                self.data = [_.text.split('\n') for _ in driver.find_elements(By.TAG_NAME, 'tr')[1:]]
                break

        driver.close()

        self.data = [[_[2], _[3], _[6], _[7]] for _ in self.data]
        self.data = {Pair: {'Price': Price, 'Volume': Volume, 'Liq': Liq} for Pair, Price, Volume, Liq in self.data}

        with open(f'ExchangesData/{exchange}', 'w+', encoding='utf-8') as file:
            file.write(str(self.data).replace('´', '').replace('Đ', 'D'))
            print(f'{cl.BRIGHT_WHITE}{NowTime()}{cl.BRIGHT_MAGENTA} ' + exchange + ' DONE!')
            del self.data, options, driver

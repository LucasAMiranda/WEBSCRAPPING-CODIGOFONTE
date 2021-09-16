import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from get_gecko_driver import GetGeckoDriver
from selenium.webdriver.firefox.options import Options
import json

get_driver = GetGeckoDriver()
get_driver.install()

# 1 - Pegar o conteúdo do Html a partir da URL
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"

option = Options()
option.headless = True
driver = webdriver.Firefox()

driver.get(url)
time.sleep(10)

#clique do botão na pontuação
driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

#Pegando elemento
element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
#capturando o Html
html_content = element.get_attribute("outerHTML")

# 2 - Tratamento dos dados - Parser do conteúdo HTML - BeatifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# 3 - Estrutura conteúdo em um DataFrame -  Pandas
#rastreando as 10 primeiras colunas na tabela

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']

print(df)

driver.quit()

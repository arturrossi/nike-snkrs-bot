import selenium
import logging
import time
import os
import argparse
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


NIKE_HOME_PAGE = "https://www.nike.com.br"
SHOE_LINK = "https://www.nike.com.br/Produto/Tenis-Nike-Joyride-Dual-Run-Feminino/1-16-19-183840#"


def login(email, password):
    logging.info('RODANDO SCRIPT DA CONTA %s' % email)

    logging.info('Entrando na pagina da NIKE')
    driver.get(NIKE_HOME_PAGE)

    disponivel = True

    while disponivel:
        try:
            logging.info('Esperando link para logar na conta NIKE')
            WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "anchor-acessar")))
        except TimeoutException:
            logging.info('Link nao apareceu, dando refresh')
            driver.refresh()
        disponivel = False


    logging.info('Clickando no Link para logar')
    driver.find_element_by_id("anchor-acessar").click()

    logging.info('Esperando campos de email e senha aparecerem')
    WebDriverWait(driver, 10000, 0.01).until(EC.visibility_of_element_located((By.XPATH, "//input[@name='emailAddress']")))
    logging.info('Preenchendo campos de email e senha')
    email_input = driver.find_element_by_xpath("//input[@name='emailAddress']")
    email_input.clear()
    email_input.send_keys(email)

    senha_entrada = driver.find_element_by_xpath("//input[@name='password']")
    senha_entrada.clear()
    senha_entrada.send_keys(password)
    logging.info('Campos de login preenchidos')


    logging.info('Clickando em entrar')
    driver.find_element_by_xpath("//input[@value='ENTRAR']").click()

    logging.info('Esperando logar')
    WebDriverWait(driver, 10000, 0.01).until(EC.visibility_of_element_located((By.CLASS_NAME, "minha-conta")))
    logging.info('Logado')

def shoe_size_add_cart(size):
    logging.info('Entrando no link do tenis')
    driver.get(SHOE_LINK)

    try:
        logging.info('Esperando tamanho do tenis aparecer')
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='tamanho__id%d']" % size)))
    except TimeoutException:
        logging.info('Link nao apareceu, dando refresh')
        driver.refresh()

    driver.find_element_by_xpath("//label[@for='tamanho__id%d']" % size).click()
    logging.info('Tamanho escolhido')

    logging.info('Esperando botao comprar estar disponivel ao click')
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.ID, "btn-comprar")))
    logging.info('Clickando em comprar')
    driver.find_element_by_id("btn-comprar").click()

    logging.info('Esperando botao de ir ao carrinho estar disponivel ao click')
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.nike.com.br/Carrinho']")))
    logging.info('Indo para o carrinho')
    driver.find_element_by_xpath("//a[@href='https://www.nike.com.br/Carrinho']").click()

def checkout():
    logging.info('Esperando botao de ir ao checkout ficar disponivel ao click')
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Continuar']")))
    logging.info('Indo ao checkout')
    driver.find_element_by_xpath("//a[text()='Continuar']").click()

    logging.info('Esperando opcao de seguir ao pagamento ficar disponivel ao click')
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.ID, "seguir-pagamento")))
    logging.info('Seguindo ao pagamento...')
    driver.find_element_by_id("seguir-pagamento").click()

    logging.info('Esperando botao para seguir para opcoes de pagamento ficar disponivel')
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[@class='modal fade ModalCorpoCentralizado show']/div/div/div[3]/button[1]")))
    logging.info('Indo às opcoes de pagamento')
    driver.find_element_by_xpath("/html/body/div[@class='modal fade ModalCorpoCentralizado show']/div/div/div[3]/button[1]").click()
    WebDriverWait(driver, 10000, 0.1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[@class='modal fade ModalCorpoCentralizado show']/div/div/div[1]/button[1]")))
    logging.info('Fechando popup chato')
    driver.find_element_by_xpath("/html/body/div[@class='modal fade ModalCorpoCentralizado show']/div/div/div[1]/button[1]").click()


    logging.info('Esperando campo do numero do cartao de credito ficar disponivel')
    WebDriverWait(driver, 10000, 0.1).until(EC.visibility_of_element_located((By.ID, "ccard-number")))
    cartao = driver.find_element_by_id("ccard-number")
    cartao.clear()
    logging.info('Preenchendo numero do cartao de credito')
    cartao.send_keys(cc_number)

    nome_cartao = driver.find_element_by_id("ccard-owner")
    nome_cartao.clear()
    logging.info('Preenchendo nome do dono do cartao de credito')
    nome_cartao.send_keys(name)

    cpf_cartao = driver.find_element_by_id("ccard-document")
    cpf_cartao.clear()
    logging.info('Preenchendo cpf')
    cpf_cartao.send_keys(cpf)

    data = validade.split('/')
    mes = data[0]
    ano = data[1]

    WebDriverWait(driver, 10000, 0.1).until(EC.invisibility_of_element_located((By.XPATH, "//div[@id='blockui-mask']")))
    mes_html = Select(driver.find_element_by_id("exp-month"))
    logging.info('Preenchendo mes de validade do cartao de credito')
    mes_html.select_by_value(mes)

    ano_html = Select(driver.find_element_by_id("exp-year"))
    logging.info('Preenchendo ano de validade do cartao de credito')
    ano_html.select_by_value(ano)

    cod_int = int(cod)
    cod_seg = driver.find_element_by_id("security-code")
    cod_seg.clear()
    logging.info('Preenchendo codigo de segurança do cartao de credito')
    cod_seg.send_keys(cod_int)

    checkbox = driver.find_element_by_id("politica-trocas")
    actions = ActionChains(driver)
    actions.move_to_element(checkbox).perform()
    driver.execute_script("arguments[0].click()", checkbox)
    logging.info('Preenchendo checkbox de politica de trocas')

    logging.info('Confirmando pagamento')
    driver.find_element_by_id("confirmar-pagamento").click()
    logging.info('Esperando o aviso de Aguarde sair da tela')
    WebDriverWait(driver, 10000, 0.1).until(EC.invisibility_of_element_located((By.XPATH, "//div[@id='blockui-mask']")))
    logging.info('Tirando print da tela')
    driver.save_screenshot(r"C:\Users\Pichau\PycharmProjects\lu\venv\%s" % args.profile + ".png")
    logging.info('Processo finalizado')
    driver.close()
    driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--profile", required=True)
    parser.add_argument("--proxy", default=None)

    args = parser.parse_args()

    #with open(args.profile, 'r') as profile:
        #linhas = profile.read().splitlines()
    linhas = []

    with open(args.profile) as profile_csv:
        profile_csv = csv.reader(profile_csv, delimiter=',')
        for coluna in profile_csv:
            linhas.extend(coluna)

    email = linhas[0]
    password = linhas[1]
    size = int(linhas[2])
    cc_number = int(linhas[3])
    name = str(linhas[4])
    cpf = str(linhas[5])
    validade = linhas[6]
    cod = int(linhas[7])

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level="INFO")

    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument('--proxy-server=%s' % args.proxy)
    driver = webdriver.Firefox(options=options)

    login(email, password)
    shoe_size_add_cart(size)
    checkout()
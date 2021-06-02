from selenium import webdriver
from time import sleep
import pandas as pd
import time


tempo_inicial = time.time()
# Pegando Dados da Planilhas
df = pd.read_excel('./infos.xlsx')
name = df['Nome'].tolist()
lastname = df['Sobrenome'].tolist()
mail = df['E-mail'].tolist()
password = df['Senha'].tolist()

# Definindo o navegador
navegador = webdriver.Firefox()

# Entrando no site
navegador.get("https://webvalidade.com/login")

# Fazendo Login
navegador.find_element_by_xpath('//*[@id="sign_in"]/div[3]/div/input').send_keys("iaravictor1312@gmail.com")
navegador.find_element_by_xpath('//*[@id="sign_in"]/div[4]/div/input').send_keys("hirozaki1312")
navegador.find_element_by_xpath('//*[@id="sign_in"]/div[5]/div[2]/button').click()
sleep(5)

# Entrando na página de criação de contas
navegador.find_element_by_xpath('/html/body/div[2]/div[1]/section/div/div[1]/div[8]/a/div/div/span[2]').click()
sleep(5)
navegador.find_element_by_xpath('//*[@id="form1"]/nav/ul/div[1]/a[4]/i').click()
sleep(5)

# Criando as contas
for nome, sobrenome, email, senha in zip(name, lastname, mail, password):
    # Escrevendo o email e a senha
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-0"]/div[1]/div/input').send_keys(email)
    navegador.find_element_by_xpath('//*[@id="password"]').send_keys(senha)
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-0"]/div[3]/div/input').send_keys(senha)
    # Passando para a próxima página
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation"]/div[3]/ul/li[2]/a').click()
    sleep(5)
    # Escrevendo o nome e sobrenome
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-1"]/div[1]/div/input').send_keys(nome)
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-1"]/div[2]/div/input').send_keys(sobrenome)
    # Confirmando a criação da conta
    navegador.find_element_by_xpath('//*[@id="wizard_with_validation"]/div[3]/ul/li[3]/a').click()
    sleep(5)

# Fechando o navegador
navegador.close()

tempo_total = (time.time() - tempo_inicial)
print(f"Tempo de duração: {tempo_total}")

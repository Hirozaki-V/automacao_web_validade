from tkinter import *
from tkinter import filedialog, messagebox
from selenium import webdriver
import pandas as pd
import time
from time import sleep
import re


class Janela:
    def __init__(self, master=None):
        # Containers
        self.firstContainer = Frame()
        self.firstContainer.pack()
        self.secondContainer = Frame()
        self.secondContainer.pack()
        self.showPathContainer = Frame()
        self.showPathContainer.pack()
        self.thirdContainer = Frame()
        self.thirdContainer.pack()

        # Login
        self.mailLabel = Label(self.firstContainer, text="E-mail para Login:")
        self.mailLabel.grid(row=0, column=0)
        self.mailEntry = Entry(self.firstContainer)
        self.mailEntry.grid(row=0, column=1)

        self.passwordLabel = Label(self.firstContainer, text="Senha para Login:")
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry = Entry(self.firstContainer, show='*')
        self.passwordEntry.grid(row=1, column=1)
        self.showPassword = Button(self.firstContainer, text="Mostrar Senha")
        self.showPassword["command"] = self.show_pass
        self.showPassword.grid(row=1, column=2)

        # Botão selecionar Planilha
        self.selectLabel = Label(self.secondContainer, text="Selecione a Planilha (.xlsx):")
        self.selectLabel.grid(row=0, column=0)
        self.selectButton = Button(self.secondContainer, text="Selecionar")
        self.selectButton["command"] = self.upload_excel
        self.selectButton.grid(row=0, column=1)

        # Monstrar caminho planilha
        self.showPath = Label(self.showPathContainer, text="")
        self.showPath.pack()

        # Botão cadastro de usuários
        self.registerButton = Button(self.thirdContainer, text="Cadastar Usuários")
        self.registerButton["command"] = self.register
        self.registerButton.grid()

    # Função para mostrar senha
    def show_pass(self):
        if self.showPassword["text"] == "Mostrar Senha":
            self.showPassword["text"] = "Esconder Senha"
            self.passwordEntry["show"] = ""
        else:
            self.showPassword["text"] = "Mostrar Senha"
            self.passwordEntry["show"] = "*"

    def upload_excel(self):
        global path, filename
        filename = filedialog.askopenfilename(title="Select a File", filetype=(("Excel", "*.xlsx"), ("Excel", "*.xls")))
        self.showPath["text"] = filename
        return filename

    # Função para validar o e-mail
    def is_email(self, data):
        emailre = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return emailre.match(data) != None

    def register(self):
        # Verificando se o diretório já foi selecionado
        try:
            filename1 = filename
        except:
            messagebox.showerror("Erro!", "Por favor, selecione o caminho da Planilha!")
        else:
            # Pegando os textos das caixas de entrada
            email = self.mailEntry.get()
            password = self.passwordEntry.get()
            is_email = self.is_email(email)
            # Mostrar mensagem de erro caso o e-mail não seja válido
            if not is_email:
                messagebox.showerror("Erro!", "Por favor, digite um e-mail válido!")
            # Mostrar mensagem de erro caso a senha esteja em branco
            elif password == "":
                messagebox.showerror("Erro!", "Por favor, não deixe os campos em branco!")
            else:
                # Pegando Dados da Planilhas
                df = pd.read_excel(filename1)
                name = df['Nome'].tolist()
                lastname = df['Sobrenome'].tolist()
                mail = df['E-mail'].tolist()
                password1 = df['Senha'].tolist()

                # Definindo o navegador
                navegador = webdriver.Firefox()

                # Entrando no site
                navegador.get("https://webvalidade.com/login")

                # Fazendo Login
                navegador.find_element_by_xpath('//*[@id="sign_in"]/div[3]/div/input').send_keys(email)
                navegador.find_element_by_xpath('//*[@id="sign_in"]/div[4]/div/input').send_keys(password)
                navegador.find_element_by_xpath('//*[@id="sign_in"]/div[5]/div[2]/button').click()
                sleep(5)

                # Entrando na página de criação de contas
                navegador.find_element_by_xpath(
                    '/html/body/div[2]/div[1]/section/div/div[1]/div[8]/a/div/div/span[2]').click()
                sleep(5)
                navegador.find_element_by_xpath('//*[@id="form1"]/nav/ul/div[1]/a[4]/i').click()
                sleep(5)

                # Criando as contas
                for nome, sobrenome, email1, senha in zip(name, lastname, mail, password1):
                    # Escrevendo o email e a senha
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-0"]/div[1]/div/input').send_keys(
                        email1)
                    navegador.find_element_by_xpath('//*[@id="password"]').send_keys(senha)
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-0"]/div[3]/div/input').send_keys(
                        senha)
                    # Passando para a próxima página
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation"]/div[3]/ul/li[2]/a').click()
                    sleep(5)
                    # Escrevendo o nome e sobrenome
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-1"]/div[1]/div/input').send_keys(
                        nome)
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation-p-1"]/div[2]/div/input').send_keys(
                        sobrenome)
                    # Confirmando a criação da conta
                    navegador.find_element_by_xpath('//*[@id="wizard_with_validation"]/div[3]/ul/li[3]/a').click()
                    sleep(5)

                # Fechando o navegador
                navegador.close()

                # Mostrando mensagem de finalização
                messagebox.showinfo("Fim!", "Usuários cadastrados com sucesso!")


root = Tk()
root.geometry("400x150")
root.resizable(False, False)
root.title("Cadastro automático WebValidade v2")
Janela(root)
root.mainloop()

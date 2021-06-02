from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.tix import *
from selenium import webdriver
import pandas as pd
import re
from time import sleep


class Janela:
    def __init__(self, master=None):
        # Containers
        self.titleContainer = Frame()
        self.titleContainer.pack()
        self.firstContainer = Frame()
        self.firstContainer.pack()
        self.secondContainer = Frame()
        self.secondContainer.pack()
        self.showPathContainer = Frame()
        self.showPathContainer.pack()
        self.thirdContainer = Frame(bd=2, relief='groove')
        self.thirdContainer.pack(pady=20)
        self.fourthContainer = Frame()
        self.fourthContainer.pack()

        # Titulo
        self.titleLabel = Label(self.titleContainer, text="Automação WebValidade")
        self.titleLabel["font"] = "Arial 20 bold"
        self.titleLabel.pack(pady=20)
        # Login
        self.mailLabel = Label(self.firstContainer, text="E-mail para Login:")
        self.mailLabel.grid(row=0, column=0)
        self.mailEntry = Entry(self.firstContainer)
        self.mailEntry.grid(row=0, column=1, ipadx=25)

        self.passwordLabel = Label(self.firstContainer, text="Senha para Login:")
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry = Entry(self.firstContainer, show='*')
        self.passwordEntry.grid(row=1, column=1, padx=20, ipadx=25)
        self.showPassword = Button(self.firstContainer, text="Mostrar Senha")
        self.showPassword["command"] = self.show_pass
        self.showPassword.grid(row=1, column=2, pady=10)

        # Botão selecionar Planilha
        self.selectLabel = Label(self.secondContainer, text="Selecione a Planilha (.xlsx):")
        self.selectLabel.grid(row=0, column=0)
        self.selectButton = Button(self.secondContainer, text="Selecionar")
        self.selectButton["command"] = self.upload_excel
        self.selectButton.grid(row=0, column=1, pady=5, padx=10)

        # Monstrar caminho planilha
        self.showPath = Label(self.showPathContainer, text="")
        self.showPath.pack(pady=13)

        # Digitar o nome das células
        tip = Balloon(root)  # Criando um tooltip
        self.help = Label(self.thirdContainer, text="i", bd=1, relief='raised', width=3, height=1)
        self.help.grid(row=0, column=5)
        tip.bind_widget(self.help, balloonmsg="Escreva os nomes referente ao nome das células da coluna na planilha.")
        self.ghost = Label(self.thirdContainer, text="", width=3, height=1)
        self.ghost.grid(row=3, column=0)
        self.nameLabel = Label(self.thirdContainer, text="Nome:")
        self.nameLabel.grid(row=1, column=1)
        self.nameEntry = Entry(self.thirdContainer)
        self.nameEntry.grid(row=1, column=2, padx=20, pady=5)
        self.lastnameLabel = Label(self.thirdContainer, text="Sobrenome:")
        self.lastnameLabel.grid(row=2, column=1)
        self.lastnameEntry = Entry(self.thirdContainer)
        self.lastnameEntry.grid(row=2, column=2)
        self.cellMailLabel = Label(self.thirdContainer, text="E-Mail:")
        self.cellMailLabel.grid(row=1, column=3)
        self.cellMailEntry = Entry(self.thirdContainer)
        self.cellMailEntry.grid(row=1, column=4)
        self.passwordCellLabel = Label(self.thirdContainer, text="Senha:")
        self.passwordCellLabel.grid(row=2, column=3)
        self.passwordCellEntry = Entry(self.thirdContainer)
        self.passwordCellEntry.grid(row=2, column=4, padx=30)

        # Botão cadastro de usuários
        self.registerButton = Button(self.fourthContainer, text="Cadastar Usuários")
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
        return emailre.match(data) is not None

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
            cellName = self.nameEntry.get()
            cellLastName = self.lastnameEntry.get()
            cellMail = self.cellMailEntry.get()
            cellPassword = self.passwordCellEntry.get()
            # Mostrar mensagem de erro caso o e-mail não seja válido
            if not is_email:
                messagebox.showerror("Erro!", "Por favor, digite um e-mail válido!")
            # Mostrar mensagem de erro caso a senha esteja em branco
            elif password == "" or cellName == "" or cellLastName == "" or cellMail == "" or cellPassword == "":
                messagebox.showerror("Erro!", "Por favor, não deixe os campos em branco!")
            else:
                # Pegando Dados da Planilhas
                df = pd.read_excel(filename1)
                name = df[cellName].tolist()
                lastname = df[cellLastName].tolist()
                mail = df[cellMail].tolist()
                password1 = df[cellPassword].tolist()

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
root.geometry("710x450")
root.resizable(False, False)
root.title("Cadastro automático WebValidade v3")
Janela(root)
root.mainloop()

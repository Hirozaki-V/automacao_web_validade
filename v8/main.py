from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from tkhtmlview import HTMLLabel
from selenium import webdriver
import pandas as pd
import re
from time import sleep
import csv
from PIL import Image, ImageTk


# criando SplashScreen
class Waiting:
    def __init__(self, master=None):
        self.firstContainer = Frame()
        self.firstContainer.pack()

        # Colocando imagem na tela
        x = './files/logo/banner.png'
        img = Image.open(x)
        img = img.resize((900, 380), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.firstContainer, image=img)
        panel.image = img
        panel.pack(side=TOP)

        # Colocando barra de progresso na tela
        pro = ttk.Progressbar(self.firstContainer, orient=HORIZONTAL, mode="determinate", length=900)
        pro.pack(side=BOTTOM)
        t = 0
        while t < 100:
            pro['value'] += 20
            root.update_idletasks()
            t += 20
            sleep(0.5)
        else:
            root.after(100, self.task)

    def task(self):
        sleep(2)
        root.destroy()

        root1 = Tk()
        root1.geometry(self.center(root1))
        root1.resizable(False, False)
        root1.iconbitmap('./files/icone/icone.ico')
        root1.title("Cadastro automático WebValidade v8")
        Janela(root)
        root1.mainloop()

    # Centralizando a tela
    @staticmethod
    def center(win):
        win.update_idletasks()
        width = 710  # win.winfo_width()
        height = 450  # win.winfo_height()
        x = int((win.winfo_screenwidth() / 2) - (width / 2))
        y = int((win.winfo_screenheight() / 2) - (height / 2))
        return f"{width}x{height}+{x}+{y}"


# Criando janela principal
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
        # Checkbutton lembrar dados
        self.rememberVar = IntVar()
        self.rememberCheck = Checkbutton(self.firstContainer, text="Lembrar dados", variable=self.rememberVar,
                                         onvalue=1, offvalue=0)
        self.rememberCheck["command"] = self.remember_data
        self.rememberCheck.grid(row=0, column=2)

        self.passwordLabel = Label(self.firstContainer, text="Senha para Login:")
        self.passwordLabel.grid(row=1, column=0)
        self.passwordEntry = Entry(self.firstContainer, show='*')
        self.passwordEntry.grid(row=1, column=1, padx=20, ipadx=25)
        # Checknutton mostrar senha
        self.isCheck = IntVar()
        self.showPassword = Checkbutton(self.firstContainer, text="Mostrar Senha", variable=self.isCheck,
                                        onvalue=1, offvalue=0)
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
        self.help = Button(self.thirdContainer, text="i", bd=1, relief="ridge", width=3, height=1)
        self.help['command'] = self.open_info
        self.help.grid(row=0, column=5)
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
        self.registerButton.grid(row=0, column=0)

        # Botão Mostrar Planilha
        self.open = Button(self.fourthContainer, text="Visualizar Planilha")
        self.open["command"] = self.show
        self.open.grid(row=0, column=1)

        self.verificar_dados()

    # Abrir janela de ajuda
    def open_info(self):
        window = Window(self)
        window.grab_set()

    # Abrir janela de visualização da planilha
    def show(self):
        try:
            filename1 = filename
        except:
            messagebox.showerror("Erro!", "Por favor, selecione o caminho da Planilha!")
        else:
            cell_name = self.nameEntry.get()
            cell_last_name = self.lastnameEntry.get()
            cell_mail = self.cellMailEntry.get()
            cell_password = self.passwordCellEntry.get()
            if cell_name == "" or cell_last_name == "" or cell_mail == "" or cell_password == "":
                messagebox.showerror("Erro!", "Por favor, não deixe os campos em branco!")
            else:
                try:
                    # Pegando Dados da Planilhas
                    df = pd.read_excel(filename1)
                    name = df[cell_name].tolist()
                    lastname = df[cell_last_name].tolist()
                    mail = df[cell_mail].tolist()
                    password1 = df[cell_password].tolist()
                 except:
                     messagebox.showerror("Erro!", "Por favor, certifique se os nomes das colunas estão corretos")
                
        dados = zip(name, lastname, mail, password1)
        nome_planilha = self.showPath.cget("text")

        window = Show(self, dados=dados, nome_planilha=nome_planilha)
        window.grab_set()

    # Verifica se a checkbox está marcada para ler o arquivo CSV
    def verificar_dados(self):
        try:
            with open('./files/data.csv', encoding='utf-8') as csv_file:
                # 2. ler a tabela
                table = csv.reader(csv_file, delimiter=',')

                # 3. navegar pela tabela
                for line in table:
                    check = line[0]
                    mail = line[1]
                    password = line[2]
                    cell_name = line[3]
                    cell_last_name = line[4]
                    cell_mail = line[5]
                    cell_password = line[6]
                if check == '1':
                    self.rememberCheck.select()
                    self.mailEntry.insert(END, mail)
                    self.passwordEntry.insert(END, password)
                    self.nameEntry.insert(END, cell_name)
                    self.lastnameEntry.insert(END, cell_last_name)
                    self.cellMailEntry.insert(END, cell_mail)
                    self.passwordCellEntry.insert(END, cell_password)

        except Exception as inst:
            print(f'Erro ao ler o arquivo .csv {inst}')
        else:
            self.mailEntry.delete(END)
            self.passwordEntry.delete(END)

    # Função para guardar os dados
    def remember_data(self):
        if self.rememberVar.get() == 1:
            # 1. cria o arquivo
            f = open('./files/data.csv', 'w', newline='', encoding='utf-8')
            # 2. cria o objeto de gravação
            w = csv.writer(f)
            # 3. grava as linhas
            w.writerow([self.rememberVar.get(), self.mailEntry.get(), self.passwordEntry.get(), self.nameEntry.get(),
                        self.lastnameEntry.get(), self.cellMailEntry.get(), self.passwordCellEntry.get()])
        if self.rememberVar.get() == 0:
            # 1. cria o arquivo
            f = open('./files/data.csv', 'w', newline='', encoding='utf-8')
            # 2. cria o objeto de gravação
            w = csv.writer(f)
            # 3. grava as linhas
            w.writerow([self.rememberVar.get(), self.mailEntry.get(), self.passwordEntry.get()])

    # Função para mostrar senha
    def show_pass(self):
        if self.isCheck.get() == 0:
            self.passwordEntry["show"] = "*"
        if self.isCheck.get() == 1:
            self.passwordEntry["show"] = ""

    # Função para escolhe o arquivo .xlsx
    def upload_excel(self):
        global path, filename
        filename = filedialog.askopenfilename(title="Select a File", filetype=(("Excel", "*.xlsx"), ("Excel", "*.xls")))
        self.showPath["text"] = filename
        return filename

    @staticmethod
    def is_email(data):
        emailre = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return emailre.match(data) is not None

    # Função para fazer o cadastro
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
            cell_name = self.nameEntry.get()
            cell_last_name = self.lastnameEntry.get()
            cell_mail = self.cellMailEntry.get()
            cell_password = self.passwordCellEntry.get()
            # Mostrar mensagem de erro caso o e-mail não seja válido
            if not is_email:
                messagebox.showerror("Erro!", "Por favor, digite um e-mail válido!")
            # Mostrar mensagem de erro caso a senha esteja em branco
            elif password == "" or cell_name == "" or cell_last_name == "" or cell_mail == "" or cell_password == "":
                messagebox.showerror("Erro!", "Por favor, não deixe os campos em branco!")
            else:
                # Pegando Dados da Planilhas
                df = pd.read_excel(filename1)
                name = df[cell_name].tolist()
                lastname = df[cell_last_name].tolist()
                mail = df[cell_mail].tolist()
                password1 = df[cell_password].tolist()

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
                dados = zip(name, lastname, mail, password1)

                # Criando as contas
                for nome, sobrenome, email1, senha in dados:
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


# Janela de ajuda
class Window(Toplevel):
    def __init__(self, master=None):
        super().__init__()
        self.geometry('835x235')
        self.resizable(False, False)
        self.title('Ajuda')

        text = """
<strong>Nome:</strong> Nome da coluna referente ao Nome do usuário a ser cadastrado<br>
<strong>Sobrenome:</strong> Nome da coluna referente ao Sobrenome do usuário a ser cadastrado<br>
<strong>E-mail:</strong> Nome da coluna referente ao E-mail do usuário a ser cadastrado<br>
<strong>Senha:</strong> Nome da coluna referente ao Senha do usuário a ser cadastrado<br>
        """

        HTMLLabel(self, html=text, height=8, width=90).pack(pady=20)

        Button(self, text='Ok', command=self.destroy, width=7).pack()

# Janela vizualização da planilha
class Show(Toplevel):
     def __init__(self, master=None, dados=[], nome_planilha=""):
        super().__init__()
        self.resizable(False, False)
        self.title(nome_planilha)

        self.tree = ttk.Treeview(self, columns=("nome", "sobrenome", "email", "senha"), show="headings")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("sobrenome", text="Sobrenome")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("senha", text="Senha")
        self.tree.pack()


        for nome, sobrenome, email, senha in dados:
            self.tree.insert("", END, values=(nome, sobrenome, email, senha))


# Centralizando a Splash Screen
def center(win):
    win.update_idletasks()
    width = 900  # win.winfo_width()
    height = 400  # win.winfo_height()
    x = int((win.winfo_screenwidth() / 2) - (width / 2))
    y = int((win.winfo_screenheight() / 2) - (height / 2))
    return f"{width}x{height}+{x}+{y}"


root = Tk()
root.geometry(center(root))
root.overrideredirect(True)
Waiting(root)
root.mainloop()

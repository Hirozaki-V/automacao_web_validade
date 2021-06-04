import csv

# 1. cria o arquivo
f = open('teste.csv', 'w', newline='', encoding='utf-8')

# 2. cria o objeto de gravação
w = csv.writer(f)

# 3. grava as linhas

w.writerow([1, "victorgabriel1312@gmail.com", "hirozaki1312"])

with open('teste.csv', encoding='utf-8') as csv_file:

  # 2. ler a tabela
  tabela = csv.reader(csv_file, delimiter=',')

  # 3. navegar pela tabela
  for l in tabela:
    print(l[0], l[1], l[2]) # 191149, Diego C B Mariano
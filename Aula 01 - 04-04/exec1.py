def menu():
    print("=== Lista de Tarefas ===")
    print("1 - Adicionar tarefa")
    print("2 - Visualizar tarefas")
    print("3 - Buscar tarefas por palavra-chave")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def carregar_tarefas():
    try:
        with open('tarefas.txt', 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        return []

def adicionar_tarefa():
    tarefa = input("Digite a descrição da tarefa: ")
    with open('tarefas.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(tarefa + '\n')
    print("Tarefa adicionada com sucesso!")

def visualizar_tarefas():
    try:
        with open('tarefas.txt', 'r', encoding='utf-8') as arquivo:
            tarefas = arquivo.readlines()
            if tarefas:
                print("\n=== Tarefas Cadastradas ===")
                for i, tarefa in enumerate(tarefas, 1):
                    print(f"{i}. {tarefa.strip()}")
            else:
                print("Nenhuma tarefa cadastrada.")
    except FileNotFoundError:
        print("Arquivo de tarefas não encontrado. Adicione uma tarefa primeiro.")
        
        
def buscar_tarefas():
    termo = input("Digite a palavra-chave para busca: ").lower()
    tarefas = carregar_tarefas()
    resultados = [t for t in tarefas if termo in t.lower()]
    if resultados:
        print("\n=== Resultados da Busca ===")
        for i, tarefa in enumerate(resultados, start=1):
            print(f"{i}. {tarefa}")
    else:
        print("Nenhuma tarefa encontrada com esse termo.")
        
        
def remover_tarefa():
    tarefas = carregar_tarefas()
    if not tarefas:
        print("Nenhuma tarefa para remover.")
        return

    visualizar_tarefas()
    try:
        indice = int(input("Digite o número da tarefa a remover: "))
        if 1 <= indice <= len(tarefas):
            removida = tarefas.pop(indice - 1)
            with open("tarefas.txt", 'w', encoding='utf-8') as f:
                for tarefa in tarefas:
                    f.write(tarefa + '\n')
            print(f"Tarefa removida: {removida}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Programa principal
while True:
    opcao = menu()
    if opcao == '1':
        adicionar_tarefa()
    elif opcao == '2':
        visualizar_tarefas()
        
    elif opcao == '3':
        buscar_tarefas()
    elif opcao == '0':
        print("Encerrando o programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")

ARQUIVO = 'tarefas.txt'

def exibir_menu():
    print("\n=== Gerenciador de Tarefas ===")
    print("1 - Adicionar nova tarefa")
    print("2 - Visualizar todas as tarefas")
    print("3 - Buscar tarefas por palavra-chave")
    print("4 - Remover tarefa pelo número")
    print("0 - Sair")
    return input("Escolha uma opção: ")

def adicionar_tarefa():
    descricao = input("Digite a descrição da tarefa: ")
    prioridade = input("Prioridade (baixa, média, alta): ").strip().lower()
    with open(ARQUIVO, 'a', encoding='utf-8') as f:
        f.write(f"{descricao} | {prioridade}\n")
    print("Tarefa adicionada com sucesso!")

def carregar_tarefas():
    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as f:
            return [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        return []

def visualizar_tarefas():
    tarefas = carregar_tarefas()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    print("\n=== Tarefas ===")
    for i, tarefa in enumerate(tarefas, start=1):
        print(f"{i}. {tarefa}")

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
            with open(ARQUIVO, 'w', encoding='utf-8') as f:
                for tarefa in tarefas:
                    f.write(tarefa + '\n')
            print(f"Tarefa removida: {removida}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Digite um número.")

# Loop principal
while True:
    opcao = exibir_menu()
    if opcao == '1':
        adicionar_tarefa()
    elif opcao == '2':
        visualizar_tarefas()
    elif opcao == '3':
        buscar_tarefas()
    elif opcao == '4':
        remover_tarefa()
    elif opcao == '0':
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")

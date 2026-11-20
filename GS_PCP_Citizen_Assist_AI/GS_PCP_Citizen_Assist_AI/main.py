"""Ponto de entrada: execute com python main.py. Sem bibliotecas externas."""
from pathlib import Path
from base_conhecimento import BaseConhecimento
from assistente import Assistente


PASTA = Path(__file__).resolve().parent / "data"


def main():
    base = BaseConhecimento(PASTA / "base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base, PASTA)
    while True:
        print("\n===== CITIZEN ASSIST AI =====")
        print("Orientações para jovens em busca de emprego e qualificação")
        print("1 - Fazer pergunta")
        print("2 - Navegar por categoria")
        print("3 - Ver indicadores")
        print("4 - Exportar atendimentos CSV")
        print("0 - Encerrar")
        opcao = input("Escolha (0 para sair): ").strip()
        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "4":
            assistente.exportar_csv()
        elif opcao == "0":
            assistente.avaliar_facilidade()
            assistente.exportar_csv()
            print("Programa encerrado. Este assistente NÃO é canal oficial.")
            break
        else:
            print("Opção inválida. Escolha uma das opções do menu.")


if __name__ == "__main__":
    main()

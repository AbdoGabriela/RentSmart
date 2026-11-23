# RentSmart - programa principal

from classes import Imovel, TaxaContratual, Orcamento


def ler_opcao(mensagem, opcoes_validas):
    # repete ate digitar uma opcao valida
    resposta = input(mensagem).strip().upper()
    while resposta not in opcoes_validas:
        print(f"Opção inválida! Digite uma destas: {', '.join(opcoes_validas)}")
        resposta = input(mensagem).strip().upper()
    return resposta


def ler_numero(mensagem, minimo, maximo):
    # le numero entre minimo e maximo
    while True:
        try:
            numero = int(input(mensagem))
            if numero >= minimo and numero <= maximo:
                return numero
            print(f"Digite um número de {minimo} a {maximo}.")
        except ValueError:
            print("Você não digitou um número válido!")


def perguntar_imovel():
    print("\nTipos de imóvel:")
    print("1 - Apartamento (R$ 700,00)")
    print("2 - Casa (R$ 900,00)")
    print("3 - Estúdio (R$ 1.200,00)")
    opcao = ler_opcao("Escolha o tipo (1/2/3): ", ["1", "2", "3"])

    tipos = {"1": "APARTAMENTO", "2": "CASA", "3": "ESTUDIO"}
    tipo = tipos[opcao]

    # valores padrao
    quartos = 1
    garagem = False
    vagas_estudio = 0
    possui_criancas = True

    if tipo == "APARTAMENTO" or tipo == "CASA":
        quartos = int(ler_opcao("Quantidade de quartos (1/2): ", ["1", "2"]))
        garagem = ler_opcao("Deseja vaga de garagem? (S/N): ", ["S", "N"]) == "S"

    if tipo == "APARTAMENTO":
        possui_criancas = ler_opcao("Possui crianças? (S/N): ", ["S", "N"]) == "S"

    if tipo == "ESTUDIO":
        quer_vagas = ler_opcao("Deseja estacionamento? (S/N): ", ["S", "N"]) == "S"
        if quer_vagas:
            vagas_estudio = ler_numero("Quantas vagas? (pacote mínimo de 2, até 10): ", 2, 10)

    return Imovel(tipo, quartos, garagem, vagas_estudio, possui_criancas)


def main():
    print("=" * 50)
    print("  RentSmart - Orçamento de Locação | R.M Imóveis")
    print("=" * 50)

    imovel = perguntar_imovel()
    parcelas = ler_numero("Parcelar a taxa contratual de R$ 2.000,00 em quantas vezes? (1 a 5): ", 1, 5)
    taxa = TaxaContratual(parcelas)

    orcamento = Orcamento(imovel, taxa)
    orcamento.exibir_resumo()

    try:
        arquivo = orcamento.exportar_csv()
        print(f"\nProjeção dos 12 meses salva no arquivo: {arquivo}")
    except PermissionError:
        # acontece quando o csv esta aberto no excel
        print("\nNão foi possível salvar o CSV. Feche o arquivo no Excel e rode de novo.")


main()

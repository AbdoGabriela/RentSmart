# RentSmart - classes

import csv

# precos
ALUGUEL_BASE = {
    "APARTAMENTO": 700.00,
    "CASA": 900.00,
    "ESTUDIO": 1200.00,
}

ADICIONAL_2_QUARTOS = {
    "APARTAMENTO": 200.00,
    "CASA": 250.00,
}

VALOR_GARAGEM = 300.00
VALOR_PACOTE_2_VAGAS = 250.00
VALOR_VAGA_EXTRA = 60.00
DESCONTO_SEM_CRIANCAS = 0.05


class Imovel:
    def __init__(self, tipo, quartos, garagem, vagas_estudio, possui_criancas):
        self.tipo = tipo
        self.quartos = quartos
        self.garagem = garagem
        self.vagas_estudio = vagas_estudio
        self.possui_criancas = possui_criancas
        self.aluguel_base = ALUGUEL_BASE[tipo]

    def calcular_adicional_quartos(self):
        if self.tipo != "ESTUDIO" and self.quartos == 2:
            return ADICIONAL_2_QUARTOS[self.tipo]
        return 0.0

    def calcular_estacionamento(self):
        if self.tipo == "ESTUDIO":
            # pacote de 2 vagas + vagas extras
            if self.vagas_estudio >= 2:
                vagas_extras = self.vagas_estudio - 2
                return VALOR_PACOTE_2_VAGAS + vagas_extras * VALOR_VAGA_EXTRA
            return 0.0
        if self.garagem:
            return VALOR_GARAGEM
        return 0.0

    def calcular_subtotal(self):
        return (self.aluguel_base
                + self.calcular_adicional_quartos()
                + self.calcular_estacionamento())

    def calcular_desconto(self):
        # 5% so para apartamento sem criancas
        if self.tipo == "APARTAMENTO" and not self.possui_criancas:
            return round(self.calcular_subtotal() * DESCONTO_SEM_CRIANCAS, 2)
        return 0.0

    def calcular_aluguel_mensal(self):
        return round(self.calcular_subtotal() - self.calcular_desconto(), 2)

    def __str__(self):
        if self.tipo == "ESTUDIO":
            return "Estúdio"
        return f"{self.tipo.capitalize()} de {self.quartos} quarto(s)"


class TaxaContratual:
    def __init__(self, parcelas):
        self.valor_total = 2000.00
        self.parcelas = parcelas

    def calcular_valor_parcela(self):
        return round(self.valor_total / self.parcelas, 2)

    def parcela_do_mes(self, mes):
        if mes < self.parcelas:
            return self.calcular_valor_parcela()
        elif mes == self.parcelas:
            # ultima parcela acerta os centavos
            ja_pago = self.calcular_valor_parcela() * (self.parcelas - 1)
            return round(self.valor_total - ja_pago, 2)
        else:
            return 0.0

    def __str__(self):
        return f"{self.parcelas}x de {formatar_moeda(self.calcular_valor_parcela())}"


class Orcamento:
    def __init__(self, imovel, taxa):
        self.imovel = imovel
        self.taxa = taxa

    def gerar_projecao(self):
        projecao = []
        aluguel = self.imovel.calcular_aluguel_mensal()
        for mes in range(1, 13):
            parcela = self.taxa.parcela_do_mes(mes)
            projecao.append({
                "Mes": mes,
                "Aluguel": aluguel,
                "Parcela da Taxa": parcela,
                "Total do Mes": round(aluguel + parcela, 2),
            })
        return projecao

    def exibir_resumo(self):
        imovel = self.imovel
        print("\n" + "=" * 50)
        print("      ORÇAMENTO DE LOCAÇÃO - R.M IMÓVEIS")
        print("=" * 50)
        print(f"Imóvel: {imovel}")
        print(f"Aluguel-base ................ {formatar_moeda(imovel.aluguel_base)}")
        if imovel.calcular_adicional_quartos() > 0:
            print(f"(+) Adicional 2 quartos ..... "
                  f"{formatar_moeda(imovel.calcular_adicional_quartos())}")
        if imovel.calcular_estacionamento() > 0:
            print(f"(+) Estacionamento .......... "
                  f"{formatar_moeda(imovel.calcular_estacionamento())}")
        if imovel.calcular_desconto() > 0:
            print(f"(-) Desconto 5% s/ crianças . "
                  f"{formatar_moeda(imovel.calcular_desconto())}")
        print("-" * 50)
        print(f"ALUGUEL MENSAL .............. "
              f"{formatar_moeda(imovel.calcular_aluguel_mensal())}")
        print("=" * 50)
        print("TAXA CONTRATUAL (separada do aluguel)")
        print(f"Valor total ................. {formatar_moeda(self.taxa.valor_total)}")
        print(f"Parcelamento ................ {self.taxa}")
        print("=" * 50)

    def exportar_csv(self, nome_arquivo="projecao-12-meses.csv"):
        campos = ["Mes", "Aluguel", "Parcela da Taxa", "Total do Mes"]
        with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
            escritor.writeheader()
            for linha in self.gerar_projecao():
                # troca ponto por virgula pro excel
                escritor.writerow({
                    "Mes": linha["Mes"],
                    "Aluguel": f"{linha['Aluguel']:.2f}".replace(".", ","),
                    "Parcela da Taxa": f"{linha['Parcela da Taxa']:.2f}".replace(".", ","),
                    "Total do Mes": f"{linha['Total do Mes']:.2f}".replace(".", ","),
                })
        return nome_arquivo


def formatar_moeda(valor):
    # 1140.5 -> R$ 1.140,50
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto

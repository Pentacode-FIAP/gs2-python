"""
Vizi: quando falta, o bairro avisa.
Global Solution FIAP 2026.2 - CitizenTech - Python

INTEGRANTES DO GRUPO PENTACODE - TURMA 1ESPH
Felipe Garcia RM 571741
Andre Luiz RM 573575
Guilherme Amorim RM 569024
Arthur Jircik RM 570754
Matheus Marcelino RM 571472

Arquivo unico: constantes, subalgoritmos (funcoes) e programa principal (menu).
Os dados da opcao 7 do menu sao SIMULADOS (campo "simulado" = True).
"""
import csv
import json

ARQUIVO_JSON = "relatos.json"
ARQUIVO_CSV = "relatorio_bairro.csv"

# Tuplas: valores fixos que nao mudam durante o programa
TIPOS = ("energia", "sinal", "agua", "alagamento", "transito")
GRAVIDADES = ("leve", "media", "alta")

CONFIRMACOES_PARA_CONFIRMAR = 2  # RN01
NEGACOES_PARA_RESOLVER = 3       # RN04

# Dados ficticios da demonstracao (lista criada com ajuda do Claude, IA). Cada item da lista e:
# (tipo, bairro, gravidade, fonte, horas sem servico)
DADOS_DEMO = [
    ("energia", "Capão Redondo", "alta", "sensor", 5.0),
    ("sinal", "Capão Redondo", "media", "morador", 2.0),
    ("agua", "Capão Redondo", "alta", "morador", 8.0),
    ("alagamento", "Capão Redondo", "media", "sensor", 2.0),
    ("transito", "Capão Redondo", "leve", "morador", 0.0),
    ("energia", "Itaquera", "leve", "morador", 1.0),
    ("alagamento", "Itaquera", "alta", "sensor", 3.0),
    ("transito", "Itaquera", "media", "morador", 0.0),
    ("sinal", "Itaquera", "leve", "sensor", 2.0),
    ("agua", "Itaquera", "media", "morador", 4.0),
    ("energia", "Pinheiros", "media", "sensor", 2.0),
    ("agua", "Pinheiros", "leve", "morador", 1.0),
    ("sinal", "Pinheiros", "alta", "morador", 3.0),
    ("alagamento", "Pinheiros", "media", "sensor", 5.0),
    ("transito", "Pinheiros", "leve", "morador", 0.0),
    ("energia", "Brasilândia", "alta", "sensor", 6.0),
    ("agua", "Brasilândia", "alta", "morador", 10.0),
    ("alagamento", "Brasilândia", "alta", "sensor", 4.0),
    ("sinal", "Brasilândia", "media", "morador", 3.0),
    ("transito", "Brasilândia", "media", "morador", 0.0),
    ("energia", "Santo Amaro", "leve", "morador", 1.0),
    ("sinal", "Santo Amaro", "leve", "sensor", 1.0),
    ("agua", "Santo Amaro", "media", "morador", 3.0),
    ("alagamento", "Santo Amaro", "media", "sensor", 2.0),
    ("transito", "Santo Amaro", "alta", "morador", 0.0),
    ("energia", "Campo Limpo", "media", "morador", 3.0),
    ("agua", "Campo Limpo", "alta", "morador", 6.0),
    ("sinal", "Campo Limpo", "leve", "sensor", 1.0),
    ("alagamento", "Campo Limpo", "alta", "sensor", 4.0),
    ("transito", "Campo Limpo", "media", "morador", 0.0),
    ("energia", "Guaianases", "alta", "sensor", 7.0),
    ("agua", "Guaianases", "media", "morador", 5.0),
    ("sinal", "Guaianases", "alta", "morador", 4.0),
    ("alagamento", "Guaianases", "media", "sensor", 3.0),
    ("transito", "Guaianases", "leve", "morador", 0.0),
    ("energia", "Mooca", "leve", "morador", 1.0),
    ("agua", "Mooca", "leve", "morador", 2.0),
    ("sinal", "Mooca", "media", "sensor", 2.0),
    ("alagamento", "Mooca", "media", "sensor", 3.0),
    ("transito", "Mooca", "alta", "morador", 0.0),
    ("energia", "Jabaquara", "media", "sensor", 3.0),
    ("agua", "Jabaquara", "media", "morador", 4.0),
    ("sinal", "Jabaquara", "leve", "morador", 1.0),
    ("alagamento", "Jabaquara", "leve", "sensor", 1.0),
    ("transito", "Jabaquara", "media", "morador", 0.0),
    ("energia", "Freguesia do Ó", "alta", "sensor", 5.0),
    ("agua", "Freguesia do Ó", "alta", "morador", 9.0),
    ("sinal", "Freguesia do Ó", "media", "morador", 3.0),
    ("alagamento", "Freguesia do Ó", "alta", "sensor", 5.0),
    ("transito", "Freguesia do Ó", "leve", "morador", 0.0),
]


# ---------------------------------------------------------------- arquivo
def carregar_relatos() -> list:
    """Le a lista de relatos do JSON. Se o arquivo nao existir, devolve lista vazia."""
    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            relatos = json.load(arquivo)
    except FileNotFoundError:
        relatos = []
    return relatos


def salvar_relatos(relatos: list) -> None:
    """Grava a lista de relatos no JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(relatos, arquivo, indent=4)


# ---------------------------------------------------------------- apoio
def proximo_id(relatos: list) -> int:
    """Devolve o proximo id livre."""
    maior = 0
    for relato in relatos:
        if relato["id"] > maior:
            maior = relato["id"]
    return maior + 1


def buscar_indice(relatos: list, id_relato: int) -> int:
    """Devolve a posicao do relato na lista, ou -1 se nao achar."""
    for posicao, relato in enumerate(relatos):
        if relato["id"] == id_relato:
            return posicao
    return -1


def mostrar_relato(relato: dict) -> None:
    """Mostra um relato em uma linha."""
    if relato["simulado"]:
        marca = " [SIMULADO]"
    else:
        marca = ""
    print(
        f"#{relato['id']} | {relato['tipo']} | {relato['bairro']} | "
        f"{relato['status']} | gravidade {relato['gravidade']} | "
        f"fonte {relato['fonte']} | +{relato['confirmacoes']} -{relato['negacoes']} | "
        f"{relato['horas']} h{marca}"
    )


def criar_relato(relatos: list, tipo: str, bairro: str, gravidade: str, fonte: str, simulado: bool) -> dict:
    """Monta um relato novo. Relato de sensor ja nasce confirmado (RN01)."""
    if fonte == "sensor":
        status = "confirmado"
    else:
        status = "ativo"
    relato = {
        "id": proximo_id(relatos),
        "tipo": tipo,
        "bairro": bairro,
        "gravidade": gravidade,
        "status": status,
        "fonte": fonte,
        "confirmacoes": 0,
        "negacoes": 0,
        "votantes": [],
        "horas": 0.0,
        "simulado": simulado,
    }
    return relato


def calcular_resumo(relatos: list) -> dict:
    """Soma ocorrencias e horas por bairro e por tipo (dicionario dentro de dicionario)."""
    resumo = {}
    for relato in relatos:
        bairro = relato["bairro"]
        tipo = relato["tipo"]
        if bairro not in resumo:
            resumo[bairro] = {}
        if tipo not in resumo[bairro]:
            resumo[bairro][tipo] = {"ocorrencias": 0, "horas": 0.0}
        resumo[bairro][tipo]["ocorrencias"] += 1
        resumo[bairro][tipo]["horas"] += relato["horas"]
    return resumo


# ---------------------------------------------------------------- opcoes do menu
def cadastrar_relato(relatos: list, tipo: str, bairro: str, gravidade: str) -> str:
    """Opcao 1: o morador reporta um problema (RF01). Devolve uma mensagem."""
    relato = criar_relato(relatos, tipo, bairro, gravidade, "morador", False)
    relatos.append(relato)
    salvar_relatos(relatos)
    return f"Pronto! Seu aviso ja esta no mapa. Id do relato: {relato['id']}"


def listar_relatos(relatos: list, filtro_tipo: str, filtro_bairro: str, filtro_status: str) -> None:
    """Opcao 2: lista relatos, com filtros opcionais (RF04). Filtro vazio nao filtra."""
    encontrados = 0
    for relato in relatos:
        passa = True
        if filtro_tipo != "" and relato["tipo"] != filtro_tipo:
            passa = False
        if filtro_bairro != "" and relato["bairro"].lower() != filtro_bairro:
            passa = False
        if filtro_status != "" and relato["status"] != filtro_status:
            passa = False
        if passa:
            mostrar_relato(relato)
            encontrados += 1
    if encontrados == 0:
        print("Nenhum relato encontrado.")


def votar_relato(relatos: list, id_relato: int, aparelho: str, resposta: str) -> str:
    """Opcao 3: confirmar ou negar um relato (RF02, RN01, RN02, RN04). Devolve uma mensagem."""
    posicao = buscar_indice(relatos, id_relato)
    if posicao == -1:
        return "Relato nao encontrado!"
    relato = relatos[posicao]
    if relato["status"] == "resolvido":
        return "Esse relato ja foi resolvido!"
    if aparelho in relato["votantes"]:
        return "Esse aparelho ja votou neste relato!"  # RN02

    relato["votantes"].append(aparelho)
    mensagem = "Obrigado por ajudar o bairro!"
    if resposta == "sim":
        relato["confirmacoes"] += 1
        if relato["status"] == "ativo" and relato["confirmacoes"] >= CONFIRMACOES_PARA_CONFIRMAR:
            relato["status"] = "confirmado"
            mensagem = "Relato confirmado pela comunidade!"
    elif resposta == "nao":
        relato["negacoes"] += 1
        if relato["negacoes"] >= NEGACOES_PARA_RESOLVER:
            relato["status"] = "resolvido"
            mensagem = "Varios moradores negaram. Relato marcado como resolvido."
    salvar_relatos(relatos)
    return mensagem


def resolver_relato(relatos: list, id_relato: int, horas: float) -> str:
    """Opcao 4: agente ou associacao marca o relato como resolvido (RF07, RN04). Devolve uma mensagem."""
    posicao = buscar_indice(relatos, id_relato)
    if posicao == -1:
        return "Relato nao encontrado!"
    relato = relatos[posicao]
    if relato["status"] == "resolvido":
        return "Esse relato ja estava resolvido!"
    relato["horas"] = horas
    relato["status"] = "resolvido"
    salvar_relatos(relatos)
    return "Boa noticia: o problema foi resolvido."


def mostrar_resumo(relatos: list) -> None:
    """Opcao 5: resumo por bairro, com horas sem servico (RF06)."""
    resumo = calcular_resumo(relatos)
    if len(resumo) == 0:
        print("Ainda nao ha relatos.")
        return
    for bairro in resumo:
        print(bairro)
        for tipo in resumo[bairro]:
            ocorrencias = resumo[bairro][tipo]["ocorrencias"]
            horas = resumo[bairro][tipo]["horas"]
            print(f"   {tipo}: {ocorrencias} ocorrencia(s), {horas:.1f} h sem servico")


def gerar_relatorio(relatos: list) -> str:
    """Opcao 6: grava o relatorio do bairro em CSV (RF09). Devolve uma mensagem."""
    resumo = calcular_resumo(relatos)
    if len(resumo) == 0:
        return "Ainda nao ha relatos para o relatorio."
    with open(ARQUIVO_CSV, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["bairro", "tipo", "ocorrencias", "horas_sem_servico"])
        for bairro in resumo:
            for tipo in resumo[bairro]:
                ocorrencias = resumo[bairro][tipo]["ocorrencias"]
                horas = resumo[bairro][tipo]["horas"]
                escritor.writerow([bairro, tipo, ocorrencias, horas])
    return f"Relatorio salvo em {ARQUIVO_CSV}."


def gerar_dados_simulados(relatos: list) -> str:
    """Opcao 7: cria relatos ficticios a partir da lista DADOS_DEMO (RN05). Devolve uma mensagem."""
    for dado in DADOS_DEMO:
        relato = criar_relato(relatos, dado[0], dado[1], dado[2], dado[3], True)
        horas = dado[4]
        if horas > 0:
            relato["status"] = "resolvido"
            relato["horas"] = horas
        relatos.append(relato)
    salvar_relatos(relatos)
    return f"{len(DADOS_DEMO)} relatos SIMULADOS criados."


# ---------------------------------------------------------------- programa principal
relatos = carregar_relatos()

print("""
VIZI - QUANDO FALTA, O BAIRRO AVISA
MENU PRINCIPAL
0 - SAIR
1 - Reportar problema
2 - Listar relatos
3 - Confirmar ou negar relato
4 - Marcar relato como resolvido
5 - Resumo por bairro
6 - Gerar relatorio do bairro
7 - Gerar dados simulados
""")

while True:

    escolha = input("Escolha: ")

    if escolha == "1":
        print("-" * 30)
        print("REPORTAR PROBLEMA")

        while True:
            tipo = input("Tipo (energia, sinal, agua, alagamento, transito): ").strip().lower()
            if tipo in TIPOS:
                break
            print("Tipo invalido!")

        while True:
            bairro = input("Bairro: ").strip()
            if bairro != "":
                break
            print("Digite o bairro!")

        while True:
            gravidade = input("Gravidade (leve, media, alta): ").strip().lower()
            if gravidade in GRAVIDADES:
                break
            print("Gravidade invalida!")

        print(cadastrar_relato(relatos, tipo, bairro, gravidade))

    elif escolha == "2":
        print("-" * 30)
        print("LISTAR RELATOS")
        print("Deixe em branco para nao filtrar")

        filtro_tipo = input("Tipo: ").strip().lower()
        filtro_bairro = input("Bairro: ").strip().lower()
        filtro_status = input("Status (ativo, confirmado, resolvido): ").strip().lower()

        listar_relatos(relatos, filtro_tipo, filtro_bairro, filtro_status)

    elif escolha == "3":
        print("-" * 30)
        print("CONFIRMAR OU NEGAR RELATO")

        while True:
            id_texto = input("Id do relato: ").strip()
            if id_texto.isnumeric():
                break
            print("Digite apenas numeros!")

        while True:
            aparelho = input("Codigo do seu aparelho (ex.: celular-1): ").strip().lower()
            if aparelho != "":
                break
            print("Digite o codigo do aparelho!")

        while True:
            resposta = input("Isso ainda acontece? (sim/nao): ").strip().lower()
            if resposta == "sim" or resposta == "nao":
                break
            print("Responda sim ou nao!")

        print(votar_relato(relatos, int(id_texto), aparelho, resposta))

    elif escolha == "4":
        print("-" * 30)
        print("PAINEL DO AGENTE")

        while True:
            id_texto = input("Id do relato: ").strip()
            if id_texto.isnumeric():
                break
            print("Digite apenas numeros!")

        while True:
            try:
                horas = float(input("Quantas horas durou o problema? ").replace(",", "."))
                break
            except ValueError:
                print("Digite um numero, por exemplo 2 ou 1.5")

        print(resolver_relato(relatos, int(id_texto), horas))

    elif escolha == "5":
        print("-" * 30)
        print("RESUMO POR BAIRRO")

        mostrar_resumo(relatos)

    elif escolha == "6":
        print("-" * 30)
        print("RELATORIO DO BAIRRO")

        print(gerar_relatorio(relatos))

    elif escolha == "7":
        print("-" * 30)
        print("DADOS SIMULADOS")

        print(gerar_dados_simulados(relatos))

    elif escolha == "0":
        print("Saindo...")
        break

    else:
        print("Opcao invalida!")

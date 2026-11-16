# Vizi - Quando falta, o bairro avisa

Global Solution FIAP 2026.2 - CitizenTech - Python

## INTEGRANTES DO GRUPO PENTACODE - TURMA 1ESPH

- Felipe Garcia RM 571741
- Andre Luiz RM 573575
- Guilherme Amorim RM 569024
- Arthur Jircik RM 570754
- Matheus Marcelino RM 571472

## Sobre o projeto

O Vizi e um mapa colaborativo da cidade de Sao Paulo. O morador reporta problemas de **energia, sinal/internet, agua, alagamento e transito**, outros moradores confirmam ou negam, e o bairro ganha um historico de quantas horas ficou sem servico. Esse historico ajuda a cobrar as empresas e o poder publico.

Este programa em Python simula o "cerebro" do Vizi no terminal: cadastra relatos, confirma, resolve e resume por bairro. Os sensores (ESP32) e o mapa visual fazem parte das outras entregas do projeto.

## Como rodar

1. Ter o Python 3 instalado.
2. Abrir o terminal na pasta do projeto.
3. Executar:

```
python vizi.py
```

O programa cria sozinho o arquivo `relatos.json` (dados salvos) e, na opcao 6, o `relatorio_bairro.csv`.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `vizi.py` | Programa completo (constantes, funcoes e menu) |
| `prompt.md` | Como a IA foi usada no desenvolvimento |
| `readme.md` | Este arquivo |
| `relatos.json` | Gerado ao rodar: relatos salvos |
| `relatorio_bairro.csv` | Gerado pela opcao 6: relatorio por bairro |

## Menu

| Opcao | O que faz |
|---|---|
| 1 | Reportar problema (tipo, bairro e gravidade) |
| 2 | Listar relatos, com filtros por tipo, bairro e status |
| 3 | Confirmar ou negar um relato |
| 4 | Marcar relato como resolvido, informando as horas sem servico |
| 5 | Resumo por bairro (ocorrencias e horas sem servico) |
| 6 | Gerar relatorio do bairro em CSV |
| 7 | Gerar 50 dados simulados (10 bairros) |
| 0 | Sair |

## Regras de negocio

- **Confirmacao:** um relato de morador comeca como "ativo" e vira "confirmado" com 2 confirmacoes.
- **Um voto por aparelho:** o mesmo aparelho nao pode votar duas vezes no mesmo relato.
- **Resolucao:** o relato vira "resolvido" quando o agente marca (opcao 4) ou quando recebe 3 negacoes.
- **Sensor:** relato vindo de sensor ja nasce "confirmado".
- **Dados simulados:** os dados da opcao 7 sao ficticios e aparecem marcados como `[SIMULADO]`.

## O que o programa usa

Menu com `while True`, validacao de entradas, `try/except` (horas digitadas), `if/elif/else`, `while` e `for`, funcoes com parametros e retorno, listas, tuplas, dicionarios e dicionarios aninhados, arquivos JSON e CSV.

## Limitacoes

- Nao ha expiracao automatica de relatos (exigiria data e hora).
- Nao ha mapa visual nem leitura de sensores reais neste programa.
- Os dados simulados nao representam a realidade.

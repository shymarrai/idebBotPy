from flask import Flask, request
# api do twilio com as funções do bot
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

dataFrame = pd.read_excel("base.xlsx", engine='openpyxl')

# rota do bot lá na interface do twilio

@app.route('/bot', methods=['POST'])
def bot():

    # recebendo a msg do usuario e deixando tudo maiusculo para padronizar
    incoming_msg = request.values.get('Body', '').upper()

    # associando o metodo de resposta do twilio importado a uma variavel
    resp = MessagingResponse()

    # associando o metodo para enviar a msg
    msg = resp.message()

    # verificador de resposta do bot
    responded = False

    # escolhendo primeira opção
    if 'CLASSIFICAÇÃO DE ESTADOS' in incoming_msg or '1' in incoming_msg:
        # bot respondendo
        responded = True

        # função da primeira pergunta
        response = optionOne()

        # envio de resposta
        msg.body(response)

    elif 'MELHORES INDICADORES EM' in incoming_msg or '2' in incoming_msg:

        # verificando se é um estado conhecido pelo bot
        if 'MINAS GERAIS' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionTwo('MINAS GERAIS')

            # envio de resposta
            msg.body(response)
        elif 'MATO GROSSO' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionTwo('MATO GROSSO')

            # envio de resposta
            msg.body(response)
        elif 'PARA' in incoming_msg or 'PARÁ' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionTwo('PARA')

            # envio de resposta
            msg.body(response)
        elif 'RIO GRANDE DO SUL' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionTwo('RIO GRANDE DO SUL')

            # envio de resposta
            msg.body(response)
        elif 'PERNAMBUCO' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionTwo('PERNAMBUCO')

            # envio de resposta
            msg.body(response)
        else:
            msg.body(help())

        responded = True
    elif 'PIORES INDICADORES EM' in incoming_msg or '3' in incoming_msg:

        # verificando se é um estado conhecido pelo bot
        if 'MINAS GERAIS' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionThree('MINAS GERAIS')

            # envio de resposta
            msg.body(response)
        elif 'MATO GROSSO' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionThree('MATO GROSSO')

            # envio de resposta
            msg.body(response)
        elif 'PARA' in incoming_msg or 'PARÁ' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionThree('PARA')

            # envio de resposta
            msg.body(response)
        elif 'RIO GRANDE DO SUL' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionThree('RIO GRANDE DO SUL')

            # envio de resposta
            msg.body(response)
        elif 'PERNAMBUCO' in incoming_msg:
            # bot respondendo
            responded = True

            # passando o estado para a função p/ ser filtrada a base
            response = optionThree('PERNAMBUCO')

            # envio de resposta
            msg.body(response)
        else:
            msg.body(help())

        responded = True
    elif 'CIDADES EM CRESCIMENTO' in incoming_msg or '4' in incoming_msg:
        response = optionFive()
        msg.body(response)
        responded = True

    elif 'CIDADES EM DECAIMENTO' in incoming_msg or '5' in incoming_msg:
        response = optionFive()
        msg.body(response)
        responded = True

    elif 'MAIS MATRICULAS' in incoming_msg or '6' in incoming_msg:

        response = optionSix()
        msg.body(response)
        responded = True

    if not responded:
        # caso msg do usuario desconhecida, fornecer as opções conhecidas
        msg.body(help())

    # retorna o método principal com a resposta
    return str(resp)


def optionOne():
    # passando true para mostrar o estado na resposta final e passando o titulo da resposta, 0 é pra pegar a primeira
    # linha
    result = consult(True, '1 - CLASSIFICAÇÃO DE ESTADOS','', 0)
    return result

def optionTwo(estado):
    result = consult(False, '2 - MELHORES INDICADORES EM ', estado, 0)
    return result

def optionThree(estado):
    result = consult(False, '3 - PIORES INDICADORES EM ', estado, -1)
    return result

def optionFour():
    title = '4 - CIDADES EM CRESCIMENTO'
    result = ranking(title, True, 8, 'Crescimento entre 2017 e 2019')
    return result

def optionFive():
    title = '5 - CIDADES EM DECAIMENTO'
    result = ranking(title, False, 8, 'Crescimento entre 2017 e 2019')
    return result

def optionSix():
    title = '6 - CIDADES COM MAIS MATRICULAS'
    result = ranking(title,True,2,'Matriculados')
    return result


# resposta p/ saida padrão
def help():
    response = "😔 Não entendi muito bem o que você deseja. Tente algo como:\n \
            1 * Classificação de estados\n \
            2 [estado] * Melhores indicadores em [estado]\n \
            3 [estado] * Piores indicadores em [estado]\n \
            4 * Cidades em crescimento\n \
            5 * Cidades em decaimento\n \
            6 * Mais matriculas\n \
            \n\n " \
               "ESTADOS CONHECIDOS:\n" \
               "MINAS GERAIS\n PARÁ\n MATO GROSO\n RIO GRANDE DO SUL\n PERNAMBUCO"
    return response

# faz filtros na base inteira com ou sem estado no resultado
def consult(isState, title, estado, direction):
    if isState:

        # filtrando de forma crescente e pegando da primeira linha
        # do resultado apenas as colunas 0(estado),1()cidade,2()matriculas
        # fazendo esse filtro com cada coluna e guardando em uma variavel

        #usando a base inteira
        item1 = dataFrame.sort_values(by=['Matriculados'], ascending=False).iloc[direction, [0, 1, 2]]
        item2 = dataFrame.sort_values(by=['Percentual Insuficiente'], ascending=False).iloc[direction, [0, 1, 3]]
        item3 = dataFrame.sort_values(by=['Percentual Básico'], ascending=False).iloc[direction, [0, 1, 4]]
        item4 = dataFrame.sort_values(by=['Percentual Proficiente'], ascending=False).iloc[direction, [0, 1, 5]]
        item5 = dataFrame.sort_values(by=['Percentual Avançado'], ascending=False).iloc[direction, [0, 1, 6]]
        item6 = dataFrame.sort_values(by=['Aprendizado Adequado'], ascending=False).iloc[direction, [0, 1, 7]]
        item7 = dataFrame.sort_values(by=['Crescimento entre 2017 e 2019'], ascending=False).iloc[direction, [0, 1, 8]]
    else:
        # filtrando de forma crescente e pegando da primeira linha
        # do resultado apenas as colunas, 1()cidade,2()matriculas
        # fazendo esse filtro com cada coluna e guardando em uma variavel

        # filtrando apenas pelo estado escolhido
        baseFiltered = dataFrame.loc[dataFrame['Estado'] == str(estado)]

        # usando a base parcial com o estado filtrado
        item2 = baseFiltered.sort_values(by=['Percentual Insuficiente'], ascending=False).iloc[direction, [1, 3]]
        item1 = baseFiltered.sort_values(by=['Matriculados'], ascending=False).iloc[direction, [1, 2]]
        item3 = baseFiltered.sort_values(by=['Percentual Básico'], ascending=False).iloc[direction, [1, 4]]
        item4 = baseFiltered.sort_values(by=['Percentual Proficiente'], ascending=False).iloc[direction, [1, 5]]
        item5 = baseFiltered.sort_values(by=['Percentual Avançado'], ascending=False).iloc[direction, [1, 6]]
        item6 = baseFiltered.sort_values(by=['Aprendizado Adequado'], ascending=False).iloc[direction, [1, 7]]
        item7 = baseFiltered.sort_values(by=['Crescimento entre 2017 e 2019'], ascending=False).iloc[direction, [1, 8]]

        title += str(estado).upper()


    # montando umtexto de resposta padrão com os resultados
    text_final = "****** %s ******\n\n" \
                 "*MATRÍCULAS NA 5ª SÉRIE*\n\n %s \n\n" \
                 "*PERCENTUAL INSUFICIENTE*\n\n %s%% \n\n" \
                 "*PERCENTUAL BÁSICO*\n\n %s%% \n\n" \
                 "*PERCENTUAL PROFICIENTE*\n\n %s%% \n\n" \
                 "*PERCENTUAL AVANÇADO*\n\n %s%% \n\n" \
                 "*APRENDIZADO ADEQUADO*\n\n %s%% \n\n" \
                 "*CRESCIMENTO ENTRE 2017 E 2019*\n\n %s%% \n\n" % \
                 (title, item1.to_string(name=False, dtype=False), item2.to_string(name=False, dtype=False),
                  item3.to_string(name=False, dtype=False),
                  item4.to_string(name=False, dtype=False),
                  item5.to_string(name=False, dtype=False),
                  item6.to_string(name=False, dtype=False),
                  item7.to_string(name=False, dtype=False))

    # name e dtype false são informações desnecessárias que poluíam a resposta
    return text_final

# ve o top 5
def ranking(title,direction,index, column):
    if direction:
        result0 = dataFrame.sort_values(by=[column], ascending=False).iloc[0, [0, 1, index]]
        result1 = dataFrame.sort_values(by=[column], ascending=False).iloc[1, [0, 1, index]]
        result3 = dataFrame.sort_values(by=[column], ascending=False).iloc[2, [0, 1, index]]
        result2 = dataFrame.sort_values(by=[column], ascending=False).iloc[3, [0, 1, index]]
        result4 = dataFrame.sort_values(by=[column], ascending=False).iloc[4, [0, 1, index]]

        response = "****** %s ******\n\n" \
                   "*1º LUGAR:*\n\n %s \n\n" \
                   "*2º LUGAR:*\n\n %s \n\n" \
                   "*3º LUGAR:*\n\n %s \n\n" \
                   "*4º LUGAR:*\n\n %s \n\n" \
                   "*5º LUGAR:*\n\n %s \n\n" % \
                   (title, result0.to_string(name=False, dtype=False), result1.to_string(name=False, dtype=False),
                    result2.to_string(name=False, dtype=False),
                    result3.to_string(name=False, dtype=False),
                    result4.to_string(name=False, dtype=False))
    else:
        result0 = dataFrame.sort_values(by=[column], ascending=False).iloc[-1, [0, 1, index]]
        result1 = dataFrame.sort_values(by=[column], ascending=False).iloc[-2, [0, 1, index]]
        result3 = dataFrame.sort_values(by=[column], ascending=False).iloc[-3, [0, 1, index]]
        result2 = dataFrame.sort_values(by=[column], ascending=False).iloc[-4, [0, 1, index]]
        result4 = dataFrame.sort_values(by=[column], ascending=False).iloc[-5, [0, 1, index]]

        response = "****** %s ******\n\n" \
                   "*1º LUGAR:*\n\n %s \n\n" \
                   "*2º LUGAR:*\n\n %s \n\n" \
                   "*3º LUGAR:*\n\n %s \n\n" \
                   "*4º LUGAR:*\n\n %s \n\n" \
                   "*5º LUGAR:*\n\n %s \n\n" % \
                   (title, result0.to_string(name=False, dtype=False), result1.to_string(name=False, dtype=False),
                    result2.to_string(name=False, dtype=False),
                    result3.to_string(name=False, dtype=False),
                    result4.to_string(name=False, dtype=False))
    return response

if __name__ == '__main__':
    app.run()

'''def getpremio(zipname):
    zipfilepath = './xml_zip' + '/'+ str(zipname)

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests
import re
import zipfile
from extrafuns import fun_result

def getLinhasPesq(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup (lattesxmldata, 'lxml', from_encoding= 'ISO-8859-1')

    pts = soup.find_all ('premios-titulos')

    if len(pts) == 0:
        print('Demais premios e titulos não encontrado para:', zipname)
    else:
        ls_pt_name=[]
        ls_pt_entpromot=[]
        ls_pt_year=[]

        for i in range(len(pts)):
            pt = pts[i].find_all('premio-titulo')
            if len(pt) == 0:
                print('Premios e titulos não encontrado para')
        ls_pesq = []
        ls_obj_pesq = []
        ls_yini = []
        ls_yfini = []
        ls_yin = []
        ls_yfin = []

        for j in range(len(ap)):
            data = ap[j].find_all('pesquisa-e-desenvolvimento')
            if len(data) == 0:
                print('linhas de pesquisas não encontradas')
            else:
                for k in range(len(data)):
                    dt = str(data[k])
                    result = re.search('ano-inicio="(.*)" codigo-orgao', dt)
                    cc = fun_result(result)
                    ls_yini.append(cc)


                    result = re.search('ano-fim="(.*)" ano-inicio', dt)
                    cc= fun_result(result)
                    if result is None:
                        cc = 'VAZIO'
                    else:
                        cc = result.group(1)
                    if cc == '':
                        cc = 'ATUAL'
                    ls_yfini.append(cc)

        for i in range(len(ap)):
            app = ap[i].find_all('pesquisa-e-desenvolvimento')
            if len(app) == 0:
                print('linhas de pesquisas não encontradas')
            else:
                for j in range(len(pt)):
                    prem = pt[j].find_all('premio-titulo')
                    for k in range(len(prem)):
                        pt_name = str(prem[k])

                        result = re.search('nome-do-premio-ou-titulo=\"(.*)\" nome-da-entidade-promotora', pt_name)
                        cc = fun_result(result)
                        ls_pt_name.append(cc)

                        result = re.search('nome-da-entidade-promotora=\"(.*)\" ano-da-premiacao', pt_name)
                        cc = fun_result(result)
                        ls_pt_entpromot.append(cc)

                        result = re.search('ano-da-premiacao=\"(.*)\" nome-do-premio-ou-titulo-ingles',pt_name)
                        cc = fun_result(result)
                        ls_pt_year.append(cc)



        df_pt = pd.DataFrame({'TITULO': ls_pt_name,
                               'ANO': ls_pt_year,
                               'ENTIDADE_PROMOTORA':ls_pt_entpromot
                              })
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_pt'  '.csv')
        df_pt.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(df_pt['TITULO']), ' premios e titulos')

                for l in range(len(app)):
                    ldp = app[l].find_all('linha-de-pesquisa')
                    for k in range(len(ldp)):
                        linha = str(ldp[k])
                        result = re.search('titulo-da-linha-de-pesquisa=\"(.*)\" titulo-da-linha-de-pesquisa-i',
                                             linha)
                        cc = fun_result(result)

                        ls_pesq.append(cc)
                        result = re.search('objetivos-linha-de-pesquisa=\"(.*)\" objetivos-linha-de-pesquisa-i', linha)
                        cc = fun_result(result)
                        ls_obj_pesq.append(cc)
                        ls_yin.append(ls_yini[i])
                        ls_yfin.append(ls_yfini[i])

        df_ldp = pd.DataFrame({'PESQUISA':ls_pesq,
                               'OBJECTIVE':ls_obj_pesq,
                               'YEAR_INI':ls_yin,
                               'YEAR_FIN':ls_yfin
                               })
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/'+latid+'_ldp'  '.csv')
        df_ldp.to_csv(pathfilename, index=False)
        print(pathfilename, 'gravado com', len(df_ldp['PESQUISA']),'linhas de pesquisas' )


def getProjEns(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')
    pen = soup.find_all('atividades-de-participacao-em-projeto')

    if pen ==0:
        print('atividades de participação em projeto não encontradas')
    else:
        ls_nome = []
        ls_yin = []
        ls_yfin = []
        ls_desc = []
        ls_sit = []
        ls_test = []
        for i in range(len(pen)):
            ens = pen[i].find_all('participacao-em-projeto')
            for j in range(len(ens)):
                ensino = ens[j].find_all('projeto-de-pesquisa')
                for k in range(len(ensino)):
                    qtdens = str(ensino[k])
                    cc = fun_result(re.search('natureza=(.*) nome-coordenador-certificacao', qtdens))
                    if cc == '"ENSINO"':
                        ls_test.append(cc)
                        result = re.search('descricao-do-projeto=\"(.*)\" descricao-do-projeto-i', qtdens)
                        ccc = fun_result(result)
                        ls_desc.append(ccc)

                        result = re.search('nome-do-projeto=\"(.*)\" nome-do-projeto-i', qtdens)
                        ccc = fun_result(result)
                        ls_nome.append(ccc)

                        result = re.search('ano-inicio="(.*)" data-c', qtdens)
                        ccc = fun_result(result)
                        ls_yin.append(ccc)

                        result = re.search('situacao="(.*)"><equipe', qtdens)
                        ccc = fun_result(result)
                        ls_sit.append(ccc)

                        result = re.search('ano-fim="(.*)" ano-inicio', qtdens)
                        ccc = fun_result(result)
                        if result is None:
                            ccc= 'VAZIO'
                        else:
                            ccc=result.group(1)
                        if ccc == '':
                            ccc = 'ATUAL'
                        ls_yfin.append(ccc)

def getProducoes(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml')

    ap = soup.find_all('producoes-ct-do-projeto')

    if len(ap) == 0:
        print('Producoes ct do projeto nao encontrado em', zipname)
    else:
        # lista de armazenamento de producoes
        ls_ttProd = []
        ls_tpProd = []

        for i in range(len(ap)):
            prd = ap[i].find_all('producao-ct-do-projeto')

            if len(ap) == 0:
                print('producao ct do projeto nao encontrado em', zipname)
            else:
                for j in range(len(prd)):
                    prodCT = str(prd[j])
                    result = re.search('titulo-da-producao-ct=\"(.*)\" tipo-producao-ct', prodCT)
                    cc = fun_result(result)
                    ls_ttProd.append(cc)

                    prodCT = str(prd[j])
                    result = re.search('tipo-producao-ct=\"(.*)\" titulo-da-producao-ct-i', prodCT)
                    cc = fun_result(result)
                    ls_tpProd.append(cc)

        df_prods = pd.DataFrame({'TITULO': ls_ttProd,
                                 'TIPO': ls_tpProd})
        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_prods' '.csv')
        df_prods.to_csv(pathfilename, index=False)
        print(pathfilename, 'gravado com', len(df_prods['TITULO']), 'producoes de CT')

def projDev(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml', from_encoding='ISO-8859-1')
    pdev = soup.find_all('atividades-de-participacao-em-projeto')

    if pdev == 0:
        print('atividades de participação em projeto não encontradas')
    else:
        ls_natu = []
        ls_yin = []
        ls_yfin = []
        ls_desc = []
        ls_sit = []

        for i in range(len)

'''


def getBancas(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                        from_encoding='ISO-8859-1')

# extrair PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO
    part_traba_c = soup.find_all('participacao-em-banca-trabalhos-conclusao')
# VERIFICANDO se ha participacao
    if len(part_traba_c) == 0:
        print(
            'participacao em bancas de trabalhos de conclusão não encontrada para:', zipname)
    else:
        ls_natu_banca = []
        ls_title_banca = []
        ls_year_banca = []
        ls_pais_banca = []
        ls_idioma_banca = []

        ls_nome_banca = []
        ls_codinst_banca = []
        ls_nomeinst_banca = []
        ls_orgao_banca = []

        ls_nome_part = []
        ls_ordem_partc = []
        ls_nomeCurso_banca = []
        ls_nome_cita = []
        ls_nroidcnpq = []

        keyword1 = []
        keyword2 = []
        keyword3 = []
        keyword4 = []
        keyword5 = []
        keyword6 = []

        ls_nBIGadc = []
        ls_ndAreadc = []
        ls_ndSUBadoc = []
        ls_especialidade = []

        for i in range(len(part_traba_c)):
            # PARTICIPACAO-EM-BANCA-DE-MESTRADO
            part_bancas = part_traba_c[i].find_all(
                'participacao-em-banca-de-mestrado')
            if len(part_bancas) == 0:
                print('participante em banca de mestrado nao encontrado', zipname)
            else:  # DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                for j in range(len(part_bancas)):
                    ptb = part_bancas[j].find_all(
                        'dados-basicos-da-participacao-em-banca-de-mestrado')

                    for k in range(len(ptb)):
                        dadosbanca = str(ptb[k])
                        result = re.search(
                            'natureza=\"(.*)\" pais', dadosbanca)
                        cc = fun_result(result)
                        ls_natu_banca.append(cc)
                        print(cc, '*********************************')

                        # titulo
                        result = re.search('titulo=\"(.*)\" titulo-i', dadosbanca)
                        cc = fun_result(result)
                        ls_title_banca.append(cc)
                        print(cc, '*********************************')
                        # ano
                        result = re.search('ano=\"(.*)\" doi', dadosbanca)
                        cc = fun_result(result)
                        ls_year_banca.append(cc)
                        print(cc, '*********************************')

                        # pais
                        result = re.search('pais=\"(.*)\" tipo', dadosbanca)
                        cc = fun_result(result)
                        ls_pais_banca.append(cc)
                        print(cc, '*********************************')

                        # idioma
                        result = re.search('idioma=\"(.*)\" natureza', dadosbanca)
                        cc = fun_result(result)
                        ls_idioma_banca.append(cc)
                        print(cc, '*********************************')

                        # detalhe participantes da banca
                        # DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO
                        detalhe= part_bancas[j].find_all('detalhamento-da-participacao-em-banca-de-mestrado')
                        for m in range(len(detalhe)):
                            detalhe_banca = str(detalhe[m])

                            # nome do candidato
                            result = re.search(
                                'nome-do-candidato=\"(.*)\" nome-i=', detalhe_banca)
                            cc = fun_result(result)
                            ls_nome_banca.append(cc)
                            print(cc, '*********************************')

                            # codigo da instituicao
                            result = re.search(
                                'codigo-instituicao=\"(.*)\" codigo-o', detalhe_banca)
                            cc = fun_result(result)
                            ls_codinst_banca.append(cc)
                            print(cc, '*********************************')

                            # nome instituicao
                            result = re.search(
                                'nome-instituicao=\"(.*)\" nome-o', detalhe_banca)
                            cc = fun_result(result)
                            ls_nomeinst_banca.append(cc)
                            print(cc, '*********************************')

                            # nome do orgao
                            result = re.search('nome-orgao=\"(.*)\"/>', detalhe_banca)
                            cc = fun_result(result)
                            ls_orgao_banca.append(cc)
                            print(cc, '*********************************')

                            # nome do curso
                            result = re.search(
                                'nome-curso=\"(.*)\" nome-curso-i', detalhe_banca)
                            cc = fun_result(result)
                            ls_nomeCurso_banca.append(cc)
                            print(cc, '*********************************')

                        Partcipantes = part_bancas[j].find_all('participante-banca')
                        parts = ''
                        ord = ''
                        nomeC = ''
                        nro = ''
                        for n in range(len(Partcipantes)):
                            partcipantes = str(Partcipantes[n])

                            result = re.search(
                                'nome-completo-do-participante-da-banca=\"(.*)\" nome-para', partcipantes)
                            cc = fun_result(result)
                            #
                            parts = parts + cc +';'
                            print(parts)



                            # nome-para-citacao-participante-da-banca
                            result = re.search(
                                'nome-para-citacao-do-participante-da-banca=\"(.*)\" nro-id', partcipantes)
                            cc = fun_result(result)
                            #ls_nome_cita.append(cc)
                            nomeC = nomeC + cc + ';'
                            print(nomeC)

                            # ordem participante
                            result = re.search(
                                'ordem-participante="(.*)">', partcipantes)
                            cc = fun_result(result)
                            #ls_ordem_partc.append(cc)
                            ord = ord + cc +';'
                            print(ord)


                            # nro id cnpq
                            result = re.search('nro-id-cnpq=\"(.*)\" ordem-p', partcipantes)
                            cc = fun_result(result)
                            #ls_nroidcnpq.append(cc)
                            if cc == '':
                                nro = ''
                            else:
                                nro = nro + cc + ';'
                            print(nro)

                        ls_nome_part.append(parts)
                        ls_nome_cita.append(nomeC)
                        ls_ordem_partc.append(ord)
                        ls_nroidcnpq.append(nro)

                        Palavras = part_bancas[j].find_all('palavras-chave')
                        p1 =''
                        p2 =''
                        p3 =''
                        p4 =''
                        p5 =''
                        p6 =''
                        for o in range(len(Palavras)):
                            palavras = str(Palavras[o])

                            # palavras chaves
                            result = re.search(
                                'palavra-chave-1=\"(.*)\" palavra-chave-2',palavras)
                            cc = fun_result(result)
                            #keyword1.append(cc)
                            if cc == '':
                                p1 =''
                            else:
                                p1 = p1 + cc +';'

                            result = re.search(
                                'palavra-chave-2=\"(.*)\" palavra-chave-3',palavras)
                            cc = fun_result(result)
                            #keyword2.append(cc)
                            if cc == '':
                                p2 = ''
                            else:
                                p2 = p2 + cc + ';'

                            result = re.search(
                                'palavra-chave-3=\"(.*)\" palavra-chave-4',palavras)
                            cc = fun_result(result)
                            #keyword3.append(cc)
                            if cc == '':
                                p3 = ''
                            else:
                                p3 = p3 + cc + ';'

                            result = re.search(
                                'palavra-chave-4=\"(.*)\" palavra-chave-5',palavras)
                            cc = fun_result(result)
                            #keyword4.append(cc)
                            if cc == '':
                                p4 = ''
                            else:
                                p4 = p4 + cc + ';'

                            result = re.search(
                                'palavra-chave-5=\"(.*)\" palavra-chave-6',palavras)
                            cc = fun_result(result)
                            #keyword5.append(cc)
                            if cc == '':
                                p5 = ''
                            else:
                                p5 = p5 + cc + ';'

                            result = re.search('palavra-chave-6=\"(.*)\">',palavras)
                            cc = fun_result(result)
                            #keyword6.append(cc)
                            if cc == '':
                                p6 = ''
                            else:
                                p6 = p6 + cc + ';'
                        keyword1.append(p1)
                        keyword2.append(p2)
                        keyword3.append(p3)
                        keyword4.append(p4)
                        keyword5.append(p5)
                        keyword6.append(p6)


                    areasConhec = part_bancas[j].find_all('areas-do-conhecimento')
                    # verificando se ha areas do conhecimento
                    if len(areasConhec) == 0:
                        print('areas do conhecimento nao encontradas', zipname)
                    else:
                        for l in range(len(areasConhec)):
                            conhec = areasConhec[l].find_all('area-do-conhecimento-1')
                            conhec = str(conhec)

                            # nome-grande-area-do-conhecimento
                            result = re.search(
                                'nome-grande-area-do-conhecimento="(.*)">', conhec)
                            cc = fun_result(result)
                            ls_nBIGadc.append(cc)
                            print(ls_nBIGadc)

                            # NOME-DA-AREA-DO-CONHECIMENTO
                            result = re.search(
                                'nome-da-area-do-conhecimento=\"(.*)\" nome-da-especialidade', conhec)
                            cc = fun_result(result)
                            ls_ndAreadc.append(cc)
                            print(ls_ndAreadc)

                            # nome-da-sub-area-do-conhecimento
                            result = re.search(
                                'nome-da-sub-area-do-conhecimento=\"(.*)\" nome-g', conhec)
                            cc = fun_result(result)
                            ls_ndSUBadoc.append(cc)
                            print(ls_ndSUBadoc)

                            # nome-da-especialidade
                            result = re.search('nome-da-especialidade="(.*)" nome-da-su', conhec)
                            cc = fun_result(result)
                            ls_especialidade.append(cc)
                            print(ls_especialidade)

        # dataDrame bancas
        df_bancas = pd.DataFrame({
            'NATUREZA': ls_natu_banca,
            'TITULO': ls_title_banca,
            'ANO': ls_year_banca,
            'PAIS': ls_pais_banca,
            'IDIOMA': ls_idioma_banca,

            'NOME-DO-CANDIDATO': ls_nome_banca,
            'CODIGO_INSTITUICAO': ls_codinst_banca,
            'NOME-DA-INSTITUICAO': ls_nomeinst_banca,
            'NOME-ORGAO': ls_orgao_banca,
            'NOME-DO-CURSO': ls_nomeCurso_banca,

            'NOME-PARTICIPANTE-BANCA': ls_nome_part,
            'ORDEM-PARTICIPANTE': ls_ordem_partc,
            'NOME-CITACAO-BANCA': ls_nome_cita,
            'NRO-ID-CNPQ': ls_nroidcnpq,

            'PALAVRA-1': keyword1,
            'PALAVRA-2': keyword2,
            'PALAVRA-3': keyword3,
            'PALAVRA-4': keyword4,
            'PALAVRA-5': keyword5,
            'PALAVRA-6': keyword6,

            'NOME-GRANDE-AREA-DO-CONHECIMENTO': ls_nBIGadc,
            'NOME-DA-AREA-DO-CONHECIMENTO': ls_ndAreadc,
            'NOME-DA-SUB-AREA-DO-CONHECIMENTO': ls_ndSUBadoc,
            'NOME-DA-ESPECIALIDADE': ls_especialidade})

        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_bancMestre' '.csv')
        df_bancas.to_csv(pathfilename, index=False)
        print(pathfilename, 'gravando com', len(df_bancas['NATUREZA']), 'bancasMestrado')

def getTCC(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                        from_encoding='ISO-8859-1')


    #PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO       
    part_TCC =soup.find_all('participacao-em-banca-trabalhos-conclusao')

    if len(part_TCC) == 0:
        print('participacao em bancas de trabalhos de conclusão não encontrada para:')
    else:

        ls_natu_tcc = []
        ls_title_tcc = []
        ls_year_tcc = []
        ls_pais_tcc = []
        ls_idioma_tcc =[]

        ls_nome_tcc = []
        ls_codinst_tcc = []
        ls_nomeinst_tcc = []
        ls_codigo_tcc = []
        ls_nomeCurso_tcc = []

        ls_ncpc_tcc = []
        ls_ordem_tcc = []
        ls_cita_tcc = []


        for a in range(len(part_TCC)):
            # PARTICIPACAO-EM-BANCA-DE-APERFEICOAMENTO-ESPECIALIZACAO
            aperfe = part_TCC[a].find_all(
                'participacao-em-banca-de-aperfeicoamento-especializacao')

            # if aperfe == '"participacao-em-banca-de-aperfeicoamento-especializacao"':

            if len(aperfe) == 0:
                print(
                    'participacao-em-banca-de-aperfeicoamento-especializacao nao encontrado', zipname)
                # DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-APERFEICOAMENTO-ESPECIALIZACAO
            else:
                for b in range(len(aperfe)):
                    pbae = aperfe[b].find_all(
                        'dados-basicos-da-participacao-em-banca-de-aperfeicoamento-especializacao')

                    for c in range(len(pbae)):
                        dadosApe = str(pbae[c])

                        result = re.search(
                            'natureza=\"(.*)\" pais', dadosApe)
                        cc = fun_result(result)
                        ls_natu_tcc.append(cc)
                        # print(cc, '*********************************')

                        # titulo
                        result = re.search(
                            'titulo=\"(.*)\" titulo-i', dadosApe)
                        cc = fun_result(result)
                        ls_title_tcc.append(cc)
                        # print(cc, '*********************************')

                        # ano
                        result = re.search('ano=\"(.*)\" doi', dadosApe)
                        cc = fun_result(result)
                        ls_year_tcc.append(cc)
                        # print(cc, '************************')

                        # pais
                        result = re.search('pais=\"(.*)\" titulo="', dadosApe)
                        cc = fun_result(result)

                        ls_pais_tcc.append(cc)
                        # print(cc, '**************************')

                        # idioma
                        result = re.search(
                            'idioma=\"(.*)\" natureza', dadosApe)
                        cc = fun_result(result)
                        ls_idioma_tcc.append(cc)
                        # print(cc, '*************************')

            detalheTCC = part_TCC[a].find_all('detalhamento-da-participacao-em-banca-de-aperfeicoamento-especializacao')
            # DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-APERFEICOAMENTO-ESPECIALIZACAO
            for d in range(len(detalheTCC)):
                detalhe_TCC = str(detalheTCC[d])

                # nome do candidato
                result = re.search(
                    'nome-do-candidato="(.*)" nome-i', detalhe_TCC)
                cc = fun_result(result)
                ls_nome_tcc.append(cc)
                #print(cc + '#', '*****************')

                # codigo da instituicao
                result = re.search(
                    'codigo-instituicao="(.*)" codigo-o', detalhe_TCC)
                cc = fun_result(result)
                ls_codinst_tcc.append(cc)
                #print(cc, '****************')

                # nome instituicao
                result = re.search(
                    'nome-instituicao="(.*)" nome-o', detalhe_TCC)
                cc = fun_result(result)
                ls_nomeinst_tcc.append(cc)
                #print(cc, '********************')

                # codigo-cuso CODIGO-CURSO= CODIGO-INSTITUICAO=
                result = re.search(
                    'codigo-curso="(.*)" codigo-ins', detalhe_TCC)
                cc = fun_result(result)
                ls_codigo_tcc.append(cc)
                #print(cc, '*******************')

                # nome do curso
                result = re.search(
                    'nome-curso=\"(.*)\" nome-curso-i', detalhe_TCC)
                cc = fun_result(result)
                ls_nomeCurso_tcc.append(cc)
                #print(cc, '*******************')

                Partcipant = part_TCC[a].find_all('participante-banca')
                pats = ''
                ords = ''
                nomec = ''
                for n in range(len(Partcipant)):
                    partcipant = str(Partcipant[n])

                    result = re.search(
                        'nome-completo-do-participante-da-banca=\"(.*)\" nome-para', partcipant)
                    cc = fun_result(result)
                    #
                    pats = pats + cc + ';'
                    print(pats)

                    # nome-para-citacao-participante-da-banca
                    result = re.search(
                        'nome-para-citacao-do-participante-da-banca=\"(.*)\" nro-id', partcipant)
                    cc = fun_result(result)
                    # ls_nome_cita.append(cc)
                    nomec = nomec + cc + ';'
                    print(nomec)

                    # ordem participante
                    result = re.search(
                        'ordem-participante="(.*)">', partcipant)
                    cc = fun_result(result)
                    # ls_ordem_partc.append(cc)
                    ords = ords + cc + ';'
                    print(ords)


                ls_ncpc_tcc.append(pats)
                ls_cita_tcc.append(nomec)
                ls_ordem_tcc.append(ords)


        #<PARTICIPANTE-BANCA NOME-COMPLETO-DO-PARTICIPANTE-DA-BANCA="Eduardo Araujo Oliveira" NOME-PARA-CITACAO-DO-PARTICIPANTE-DA-BANCA="OLIVEIRA, E. A." ORDEM-PARTICIPANTE="1" NRO-ID-CNPQ=""/>

        # dataDrame bancas
        df_bancasTCC = pd.DataFrame({
        
        'NATUREZA': ls_natu_tcc,
        'TITULO':ls_title_tcc,
        'ANO':ls_year_tcc,
        'PAIS':ls_pais_tcc,
        'IDIOMA':ls_idioma_tcc,

        'NOME-DO-CANDIDATO':ls_nome_tcc,
        'CODIGO_INSTITUICAO':ls_codinst_tcc,
        'NOME-DA-INSTITUICAO':ls_nomeinst_tcc,
        'CODIGO-CURSO':ls_codigo_tcc, 
        'NOME-DO-CURSO':ls_nomeCurso_tcc,

        'NOME-C-PART-BANCA': ls_ncpc_tcc,
        'ORDEM-PARTICIPANTE': ls_ordem_tcc,
        'NOME-CITACAO' :ls_cita_tcc,
        })

        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_bancaESPE' '.csv')
        df_bancasTCC.to_csv(pathfilename, index=False)
        print(pathfilename, 'gravando com', len(df_bancasTCC['NATUREZA']), 'banca_especializacao')


def getGrad(zipname):
    zipfilepath = './xml_zip' + '/' + str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup(lattesxmldata, 'lxml',
                        from_encoding='ISO-8859-1')

# extrair PARTICIPACAO-EM-BANCA-TRABALHOS-CONCLUSAO
    partGrad = soup.find_all('participacao-em-banca-trabalhos-conclusao')
# VERIFICANDO se ha participacao
    if len(partGrad) == 0:
        print('participacao em bancas de trabalhos de conclusão não encontrada para:', zipname)
    else:
        ls_natu_Grad = []
        ls_title_Grad = []
        ls_year_Grad = []
        ls_pais_Grad = []
        ls_idioma_Grad = []

        ls_nome_Gra = []
        ls_codinst_Gra = []
        ls_nomeinst_Gra = []
        ls_orgao_Gra = []
        ls_nomeCurso_Gra = []

        ls_nomPar_Gra = []
        ls_nome_cita_Gra = []
        ls_ordem_partc_gra = []


        for i in range(len(partGrad)):
            # PARTICIPACAO-EM-BANCA-DE-MESTRADO
            part_Grad = partGrad[i].find_all( #PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                'participacao-em-banca-de-graduacao')
            if len(part_Grad) == 0:
                print('participante em banca de graduacao nao encontrado', zipname)
            else:  # DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                for j in range(len(part_Grad)):#DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                    ptGrad = part_Grad[j].find_all('dados-basicos-da-participacao-em-banca-de-graduacao')

                    for k in range(len(ptGrad)):
                        dadosGrad = str(ptGrad[k])
                        result = re.search('natureza=\"(.*)\" pais', dadosGrad)
                        cc = fun_result(result)
                        ls_natu_Grad.append(cc)
                        print(cc, '*************')

                        # titulo  xcxxc
                        result = re.search('titulo=\"(.*)\" titulo-i', dadosGrad)
                        cc = fun_result(result)
                        ls_title_Grad.append(cc)
                        print(cc, '*****************')

                        result = re.search('ano=\"(.*)\" doi', dadosGrad)
                        cc = fun_result(result)
                        ls_year_Grad.append(cc)
                        print(cc, '**********************')

                        result = re.search('pais=\"(.*)\" titulo=', dadosGrad)
                        cc = fun_result(result)
                        ls_pais_Grad.append(cc)
                        print(cc, '*****************')

                        result = re.search('idioma=\"(.*)\" natureza', dadosGrad)
                        cc = fun_result(result)
                        ls_idioma_Grad.append(cc)
                        print(cc, '*********************')

                        # DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-GRADUACAO
                    detalgradu = part_Grad[j].find_all('detalhamento-da-participacao-em-banca-de-graduacao')
                    for m in range(len(detalgradu)):
                        detalhe_Gradu = str(detalgradu[m])
                        # nome do candidato
                        result = re.search('nome-do-candidato=\"(.*)\" nome-i', detalhe_Gradu)
                        cc = fun_result(result)
                        ls_nome_Gra.append(cc)
                        print(cc, '*****************')

                            # codigo da instituicao
                        result = re.search('codigo-instituicao=\"(.*)\" codigo-orgao=', detalhe_Gradu)
                        cc = fun_result(result)
                        ls_codinst_Gra.append(cc)
                        print(cc, '****************')

                         # nome instituicao
                        result = re.search('nome-instituicao="(.*)" nome-orgao=', detalhe_Gradu)
                        cc = fun_result(result)
                        ls_nomeinst_Gra.append(cc)
                        print(cc, '*****************')

                            # nome do curso
                        result = re.search('nome-curso=\"(.*)\" nome-curso-ingles=', detalhe_Gradu)
                        cc = fun_result(result)
                        ls_nomeCurso_Gra.append(cc)
                        print(cc, '**************')

                        '''partciGra = part_Grad[j].find_all('participante-banca')
                        for l in range(len(partciGra)):
                            pGra = str(partciGra[l])
    
                            result = re.search(
                                'nome-completo-do-participante-da-banca=\"(.*)\" nome-para', pGra)
                            cc = fun_result(result)
                            ls_nomPar_Gra.append(cc)
                            print(cc)
    
                            result = re.search(
                                'nome-para-citacao-do-participante-da-banca=\"(.*)\" nro-id', pGra)
                            cc = fun_result(result)
                            ls_nome_cita_Gra.append(cc)
                            print(cc)
    
                            result = re.search('ordem-participante="(.*)">', pGra)
                            cc = fun_result(result)
                            ls_ordem_partc_gra.append(cc)
                            print(cc)'''

        df_bancGRAD = pd.DataFrame({
            'NATUREZA': ls_natu_Grad,
            'TITULO': ls_title_Grad,
            'ANO': ls_year_Grad,
            'PAIS': ls_pais_Grad,
            'IDIOMA': ls_idioma_Grad,

            'NOME-DO-CANDIDATO': ls_nome_Gra,
            'CODIGO_INSTITUICAO': ls_codinst_Gra,
            'NOME-DA-INSTITUICAO': ls_nomeinst_Gra,
            'NOME-DO-CURSO': ls_nomeCurso_Gra,

            #'NOME-PARTICIPANTE-BANCA': ls_nomPar_Gra,
            #'ORDEM-PARTICIPANTE': ls_ordem_partc_gra,
            #'NOME-CITACAO-BANCA': ls_nome_cita_Gra,

        })

        latid = zipname.split('.')[0]
        pathfilename = str('./csv_producao/' + latid + '_bancGRADU' '.csv')
        df_bancGRAD.to_csv(pathfilename, index=False)
        print(pathfilename, 'gravando com', len(df_bancGRAD['NATUREZA']), 'bancasGraduacao')


#from scraperlattes import getBancas
#from scraperlattes import getTCC
#from scraperlattes import getGrad


#getBancas(zipfilename)
#getTCC(zipfilename)
#getGrad(zipfilename)


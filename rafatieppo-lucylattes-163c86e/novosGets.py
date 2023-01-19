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
    soup= BeautifulSoup(lattesxmldata, 'lxml',
                         from_encoding='ISO-8859-1')

    ap = soup.find_all('atividades-de-pesquisa-e-desenvolvimento')
    if len(ap)==0:
        print('atividades de pesquisas não encontradas para:', zipname)
    else:
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
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
        print(pathfilename, 'gravado com', len(df_ldp['PESQUISA']),'pesquisa' )

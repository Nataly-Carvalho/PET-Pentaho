# ------------------------------------------------------------
# packages
# ------------------------------------------------------------

from extrafuns import *
from tabulate import tabulate
import numpy as np
import pandas as pd
import os
import glob
import re
import matplotlib.pyplot as plt
import matplotlib.style as style
import platform
import sys
style.available
style.use('fivethirtyeight')


def getrelatorio():
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    yyi = config_file.readlines()[5].split(':')[1]
    yyi = yyi.rstrip('\n')
    yyi = yyi.strip(' ')
    yyi = float(yyi)
    config_file.close()
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    yyf = config_file.readlines()[6].split(':')[1]
    yyf = yyf.rstrip('\n')
    yyf = yyf.strip(' ')
    yyf = float(yyf)
    config_file.close()
    # config_file = open('./config.txt', 'r')
    config_file = open('./config.txt', 'r', encoding='utf-8')
    qualqualis = config_file.readlines()[4].split(':')[1]
    qualqualis = qualqualis.rstrip('\n')
    qualqualis = qualqualis.strip(' ')
    qualqualis = str(qualqualis)
    config_file.close()
    # define como zero algumas variaveis, pois elas podem nao existir na
    # contagem
    ppe_tot, pp_tot, liv_tot, chap_tot, acp_tot = 0, 0, 0, 0, 0
    # ------------------------------------------------------------
    # verificando a existencia dos arquivos
    # importando os data frames gerados pelo gettidy
    # filtrando por ano e ordenando
    # criou-se uma variavel para controle da impressao do relatorio
    # html, caso o tipo de producao exista a variavel html_print_ppe
    # recebe YES, caso contrario NO
    # ------------------------------------------------------------
    # dfppe_all
    try:
        dfppe_all = pd.read_csv('./csv_producao/projetos_all.csv',
                                header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com producao de proj. pesq ou ext. \n' +
              '------------------------------------------------------------')
        html_print_ppe_all = 'NO'
    else:
        html_print_ppe_all = 'YES'
        dfppe_all['YEAR_INI'] = dfppe_all['YEAR_INI'].replace('VAZIO', -99)
        ppenum99 = dfppe_all[dfppe_all['YEAR_INI']
                             == -99].reset_index(drop=True)
        if len(ppenum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(ppenum99)) +
                  'projetos sem ano inicial')
            print('------------------------------------------------------------')
        # filtrando ano
        dfppe_all['YEAR_INI'] = dfppe_all['YEAR_INI'].apply(ff)
        dfppe_all = dfppe_all[(dfppe_all['YEAR_INI'] >= yyi)]
    # ------------------------------------------------------------
    # dfppe_uniq
    try:
        dfppe_uniq = pd.read_csv('./csv_producao/projetos_uniq.csv',
                                 header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com producao de proj. pesq ou ext. uniq \n' +
              '------------------------------------------------------------')
        html_print_ppe_uniq = 'NO'
    else:
        html_print_ppe_uniq = 'YES'
        dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].replace('VAZIO', -99)
        ppenum99 = dfppe_uniq[dfppe_uniq['YEAR_INI']
                              == -99].reset_index(drop=True)
        if len(ppenum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(ppenum99)) +
                  'projetos sem ano inicial')
            print('------------------------------------------------------------')
        # filtrando ano
        dfppe_uniq['YEAR_INI'] = dfppe_uniq['YEAR_INI'].apply(ff)
        dfppe_uniq = dfppe_uniq[(dfppe_uniq['YEAR_INI'] >= yyi)]
        dfppe_uniq_pesq = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'PESQUISA']
        dfppe_uniq_pesq = dfppe_uniq_pesq.sort_values(['YEAR_INI'])
        dfppe_uniq_ext = dfppe_uniq[dfppe_uniq['NATUREZA'] == 'EXTENSAO']
        dfppe_uniq_ext = dfppe_uniq_ext.sort_values(['YEAR_INI'])
        # Descritivo do numero de proj pesq e ext
        pp = dfppe_uniq_pesq.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
        pp_tot = pp['PROJ'].sum()
        ppe = dfppe_uniq_ext.groupby(['YEAR_INI'])['PROJ'].size().reset_index()
        ppe_tot = ppe['PROJ'].sum()
    # ------------------------------------------------------------
    # dfpaper all
    try:
        dfpaper = pd.read_csv('./csv_producao/periodicos_all.csv',
                              header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com peri??dico all \n' +
              '------------------------------------------------------------')
        html_print_paper_all = 'NO'
    else:
        html_print_paper_all = 'YES'
        dfpaper['YEAR'] = dfpaper['YEAR'].replace('VAZIO', -99)
        pernum99 = dfpaper[dfpaper['YEAR'] == -99].reset_index(drop=True)
        if len(pernum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(pernum99)) +
                  'artigos sem ano de publicacao')
            print('------------------------------------------------------------')
        # filtrando ano
        dfpaper['YEAR'] = dfpaper['YEAR'].apply(ff)
        dfpaper = dfpaper[(dfpaper['YEAR'] >= yyi) & (dfpaper['YEAR'] <= yyf)]
    # ------------------------------------------------------------
    # dfpaper unique
    try:
        dfpaper_uniq = pd.read_csv('./csv_producao/periodicos_uniq.csv',
                                   header=0, dtype='str')
    except (OSError, IOError):
        html_print_paper_uniq = 'NO'
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com peri??dico unique \n' +
              '------------------------------------------------------------')
    else:
        html_print_paper_uniq = 'YES'
        dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].replace('VAZIO', -99)
        pernum99 = dfpaper_uniq[dfpaper_uniq['YEAR']
                                == -99].reset_index(drop=True)
        # filtrando ano
        dfpaper_uniq['YEAR'] = dfpaper_uniq['YEAR'].apply(ff)
        dfpaper_uniq = dfpaper_uniq[(dfpaper_uniq['YEAR']
                                     >= yyi) & (dfpaper_uniq['YEAR'] <= yyf)]
        dfpaper_uniq = dfpaper_uniq.sort_values(['YEAR'])
        # GRAFICO artig completo periodico
        acp = dfpaper_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        acp_tot = acp['TITLE'].sum()
        plt.figure(figsize=(9, 5))
        plt.bar(x=acp['YEAR'], height=acp['TITLE'])
        plt.title('Publica????es %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('N??mero de publica????es')
        plt.tight_layout()
        plt.savefig('./relatorio/figures/period_dep_year.png')
        # plt.show()
        # GRAFICO artig completo periodico por qualis
        acpq = dfpaper_uniq.groupby(['QUALIS'])['TITLE'].size().reset_index()
        # acpq
        plt.figure(figsize=(9, 5))
        plt.bar(x=acpq['QUALIS'], height=acpq['TITLE'])
        plt.title('Publica????es %i - %i' % (yyi, yyf))
        plt.xlabel('Qualis')
        plt.ylabel('N??mero de publica????es')
        plt.tight_layout()
        plt.savefig('./relatorio/figures/period_year_qualis.png')
        # plt.show()
    # ------------------------------------------------------------
    # dfbooks all
    try:
        dfbooks = pd.read_csv('./csv_producao/livros_all.csv',
                              header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com livros all \n' +
              '------------------------------------------------------------')
        html_print_books_all = 'NO'
    else:
        html_print_books_all = 'YES'
        dfbooks['YEAR'] = dfbooks['YEAR'].replace('VAZIO', -99)
        booknum99 = dfbooks[dfbooks['YEAR'] == -99].reset_index(drop=True)
        if len(booknum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(booknum99)) +
                  ' livros sem ano de publicacao')
            print('------------------------------------------------------------')
        # filtrando ano
        dfbooks['YEAR'] = dfbooks['YEAR'].apply(ff)
        dfbooks = dfbooks[(dfbooks['YEAR'] >= yyi) & (dfbooks['YEAR'] <= yyf)]
    # ------------------------------------------------------------
    # dfbooks_uniq
    try:
        dfbooks_uniq = pd.read_csv('./csv_producao/livros_uniq.csv',
                                   header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com livros unique \n' +
              '------------------------------------------------------------')
        html_print_books_uniq = 'NO'
    else:
        html_print_books_uniq = 'YES'
        dfbooks_uniq['YEAR'] = dfbooks_uniq['YEAR'].replace('VAZIO', -99)
        # filtrando ano
        dfbooks_uniq['YEAR'] = dfbooks_uniq['YEAR'].apply(ff)
        dfbooks_uniq = dfbooks_uniq[(dfbooks_uniq['YEAR']
                                     >= yyi) & (dfbooks_uniq['YEAR'] <=
                                                yyf)]
        dfbooks_uniq = dfbooks_uniq.sort_values(['YEAR'])
        # Descritivo do numero de livros
        liv = dfbooks_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        liv_tot = liv['TITLE'].sum()
        # GRAFICO livros
        livp = dfbooks_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=livp['YEAR'], height=livp['TITLE'])
        plt.title('Livros  %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('N??mero de livros')
        # plt.yticks(np.arange(0, livp['TITLE'].max() + 10, 5))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/livros_dep_year.png')
        # plt.show()
    # ------------------------------------------------------------
    # dfchapters all
    try:
        dfchapters = pd.read_csv('./csv_producao/capitulos_all.csv',
                                 header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com capitulos all \n' +
              '------------------------------------------------------------')
        html_print_chapter_all = 'NO'
    else:
        html_print_chapter_all = 'YES'
        dfchapters['YEAR'] = dfchapters['YEAR'].replace('VAZIO', -99)
        chapnum99 = dfchapters[dfchapters['YEAR']
                               == -99].reset_index(drop=True)
        if len(chapnum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(chapnum99)) +
                  ' cap??tulos sem ano de publicacao')
            print('------------------------------------------------------------')
        # filtrando ano
        dfchapters['YEAR'] = dfchapters['YEAR'].apply(ff)
        dfchapters = dfchapters[(dfchapters['YEAR'] >= yyi)
                                & (dfchapters['YEAR'] <= yyf)]
    # ------------------------------------------------------------
    # dfchapters_uniq
    try:
        dfchapters_uniq = pd.read_csv('./csv_producao/capitulos_uniq.csv',
                                      header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com capitulos unique \n' +
              '------------------------------------------------------------')
        html_print_chapter_uniq = 'NO'
    else:
        html_print_chapter_uniq = 'YES'
        dfchapters_uniq['YEAR'] = dfchapters_uniq['YEAR'].replace('VAZIO', -99)
        # filtrando ano
        dfchapters_uniq['YEAR'] = dfchapters_uniq['YEAR'].apply(ff)
        dfchapters_uniq = dfchapters_uniq[(dfchapters_uniq['YEAR']
                                           >= yyi) & (dfchapters_uniq['YEAR'] <= yyf)]
        dfchapters_uniq = dfchapters_uniq.sort_values(['YEAR'])
        # Descritivo do numero de capitulos
        chap = dfchapters_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        chap_tot = chap['TITLE'].sum()
        # GRAFICO capitulos
        capp = dfchapters_uniq.groupby(['YEAR'])['TITLE'].size().reset_index()
        plt.figure(figsize=(9, 5))
        plt.bar(x=capp['YEAR'], height=capp['TITLE'])
        plt.title('Cap??tulos %i - %i' % (yyi, yyf))
        plt.xticks(np.arange(yyi, yyf + 1, 1))
        plt.xlabel('Ano')
        plt.ylabel('N??mero de cap??tulos')
        # plt.yticks(np.arange(0, capp['TITLE'].max() + 10, 5))
        plt.tight_layout()
        plt.savefig('./relatorio/figures/capitulos_dep_year.png')
        # plt.show()
    # ------------------------------------------------------------
    # dfadvise
    try:
        dfadvise = pd.read_csv('./csv_producao/orientacoes_all.csv',
                               header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com orientacoes \n' +
              '------------------------------------------------------------')
        html_print_advi = 'NO'
    else:
        html_print_advi = 'YES'
        dfadvise['YEAR'] = dfadvise['YEAR'].replace('VAZIO', -99)
        chapnum99 = dfadvise[dfadvise['YEAR'] == -99].reset_index(drop=True)
        if len(chapnum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(chapnum99)) +
                  ' orientacoes sem ano inicial')
            print('------------------------------------------------------------')
        # filtrando ano
        dfadvise['YEAR'] = dfadvise['YEAR'].apply(ff)
        dfadvise = dfadvise[(dfadvise['YEAR'] >= yyi)
                            & (dfadvise['YEAR'] <= yyf)]
        dfadvise = dfadvise.sort_values(['YEAR'])
        # Descritivo do numero de orientacoes
        advi = dfadvise.groupby(['NATURE'])['STUDENT'].size().reset_index()
        advi_tot = advi['STUDENT'].sum()
        advi.columns = ['NATUREZA', 'QTD']

    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # dfensidisc
    try:
        dfensidi = pd.read_csv('./csv_producao/ensdisc_all.csv',
                               header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com disciplinas e ensino \n' +
              '------------------------------------------------------------')
        html_print_ensidi = 'NO'
    else:
        html_print_ensidi = 'YES'
        dfensidi['YEAR_INI'] = dfensidi['YEAR_INI'].replace('VAZIO', -99)
        chapnum99 = dfensidi[dfensidi['YEAR_INI']
                             == -99].reset_index(drop=True)
        if len(chapnum99) >= 1:
            print('------------------------------------------------------------')
            print('ATENCAO: \n' + str(len(chapnum99)) +
                  ' disciplinas sem ano inicial')
            print('------------------------------------------------------------')
        # filtrando ano
        dfensidi['YEAR_INI'] = dfensidi['YEAR_INI'].apply(ff)
        dfensidi = dfensidi[(dfensidi['YEAR_INI'] >= yyi)
                            & (dfensidi['YEAR_INI'] <= yyf)]
        dfensidi = dfensidi.sort_values(['YEAR_INI'])

    # ------------------------------------------------------------
    # dfindicadores qualis indice de orientacao do grupo
    try:
        dfind_capes_indori = pd.read_csv('./csv_producao/capesindex_indori.csv',
                                         header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com com indicador capes orientados por quadrienios  \n' +
              '------------------------------------------------------------')
        html_print_indori = 'NO'
    else:
        html_print_indori = 'YES'

    # ------------------------------------------------------------
    # dfindicadores qualis indice produtividade de artigos
    try:
        dfind_capes_indprodart = pd.read_csv('./csv_producao/capesindex_indprodart.csv',
                                             header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com com indicador capes orientados por quadrienios  \n' +
              '------------------------------------------------------------')
        html_print_indprodart = 'NO'
    else:
        html_print_indprodart = 'YES'

    # ------------------------------------------------------------
    # dfindicadores qualis indice autoria discente
    try:
        dfind_capes_indautdis = pd.read_csv('./csv_producao/capesindex_indautdis.csv',
                                            header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? arquivo com com indicador capes indice autoria discente  \n' +
              '------------------------------------------------------------')
        html_print_indautdis = 'NO'
    else:
        html_print_indautdis = 'YES'
    # ------------------------------------------------------------
    # Indic distrib dos doce perman por faixa de IndProd
    try:
        dfind_capes_distindproddp = pd.read_csv('./csv_producao/capesindex_distindproddp_doce.csv',
                                                header=0, dtype='str')
    except (OSError, IOError):
        print('------------------------------------------------------------\n' +
              'ATENCAO \n' +
              'N??o h?? indicador capes de Ind. de distrib. dos docentes permanentes por faixa de IndProd  \n' +
              '------------------------------------------------------------')
        html_print_distindproddp = 'NO'
    else:
        html_print_distindproddp = 'YES'

    # ------------------------------------------------------------
    # INICIANDO o html DANGER ATTENTION PAREI AQUI
    htmlfile = open('./relatorio/relatorio_producao.html', 'w')
    htmlfile.write('<!DOCTYPE html> \n ')
    htmlfile.write('<head> \n ')
    # verificando sistema
    plat_sys = platform.system()
    if plat_sys == 'Windows':
        htmlfile.write(
            '<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1" />  \n')
    else:
        htmlfile.write(
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />  \n')
    htmlfile.write(' <title>lucyLattes Relatorio</title> \n')
    htmlfile.write(
        '<link rel="stylesheet" href="./css/gitgub.css" type="text/css" /> \n </head> \n')
    htmlfile.write('</head> \n ')
    htmlfile.write('<body> \n')
    # quick sumario
    htmlfile.write('<h0 class="title">Relat??rio de Produ????o</h0> \n <br>\n')
    htmlfile.write('<small>Gerado por <i>lucyLattes.py</i>' + ' ' +
                   '<a href="https://github.com/rafatieppo/lucyLattes">https://github.com/rafatieppo/lucyLattes</a></small> \n <br> \n')
    htmlfile.write(
        '<a href="https://doi.org/10.5281/zenodo.2591748"> <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.2591748.svg" alt="DOI"> </a>')
    htmlfile.write('<h1 class="title">Sum??rio</h1> \n')
    htmlfile.write('<a href="#team">Equipe</a> \n <br>')
    htmlfile.write('<a href="#resprod">Resumo da produ????o</a> \n <br>')
    htmlfile.write('<a href="#projexte">Projetos de extens??o</a> \n <br>')
    htmlfile.write('<a href="#projpesq">Projetos de pesquisa</a> \n <br>')
    htmlfile.write('<a href="#pubbookchap">Livros e cap??tulos</a> \n <br>')
    htmlfile.write('<a href="#pubperiod">Artigos em peri??dicos</a> \n <br>')
    htmlfile.write(
        '<a href="#prodporpesq">Extrato de peri??dicos por integrante</a> \n <br>')
    htmlfile.write('<a href="#indcapes">Indicadores CAPES</a> \n <br>')
    # Equipe
    htmlfile.write('<a name="team"></a>' + '\n \n')
    htmlfile.write('<h1 class="title">Equipe</h1> \n')
    # Descricao de cada pesquisador
    # df com nome completo, sobrenome, id, lattes update
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    # passando ID para string, para poder comparar com dfpaper
    # dfpaper['ID'] = dfpaper['ID'].apply(ss)
    # dffullname['ID'] = dffullname['ID'].apply(ss)
    # dfpaper = pd.merge(dfpaper, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    for idd in range(len(dffullname)):
        htmlfile.write('<hr>')
        htmlfile.write('<b>Nome: </b>')
        htmlfile.write(dffullname.iloc[idd, 1])
        htmlfile.write('<br>')
        htmlfile.write('<b>Nascimento: </b>')
        if pd.isna(dffullname.iloc[idd, 4]):
            htmlfile.write('no city')
        else:
            htmlfile.write(dffullname.iloc[idd, 4])
            htmlfile.write(' - ')
            htmlfile.write(str(dffullname.iloc[idd, 5]))
        htmlfile.write('<br>')
        htmlfile.write('<b>Institui????o: </b>')
        if pd.isna(dffullname.iloc[idd, 8]):
            htmlfile.write('n??o informado')
        else:
            htmlfile.write(dffullname.iloc[idd, 8])
        htmlfile.write('<br>')
        htmlfile.write('<b>Resumo: </b>')
        htmlfile.write(str(dffullname.iloc[idd, 6]))
        htmlfile.write('<p>')
        htmlfile.write('<b>Lattes: </b>')
        latteslink = 'http://lattes.cnpq.br/' + str(dffullname.iloc[idd, 0])
        htmlfile.write('<a href="' + latteslink + '">' + latteslink + '</a>')
        htmlfile.write('<br>')
        htmlfile.write('<b>??ltima atualiza????o: </b>')
        lattesupda = str(dffullname.iloc[idd, 7])
        htmlfile.write(lattesupda + '<br> <br>')
    # resumo da produ????o projetos, periodicos
    htmlfile.write('<hr> \n')
    htmlfile.write('<a name="resprod"></a>' + '\n \n')
    htmlfile.write('<h1>Resumo da Produ????o</h1> \n')
    htmlfile.write('Per??odo avaliado: ' + str(int(yyi)) +
                   ' - ' + str(int(yyf)) + '\n <br> \n')
    htmlfile.write('N??mero de membros na equipe: ' +
                   (str(len(dffullname)) + '\n <br> \n'))
    htmlfile.write('N??mero de projetos de extens??o: ' +
                   (str(ppe_tot) + '\n <br> \n'))
    htmlfile.write('N??mero de projetos de pesquisa: ' +
                   (str(pp_tot) + '\n <br> \n'))
    htmlfile.write('Livros publicados: ' +
                   (str(liv_tot) + '\n <br> \n'))
    htmlfile.write('Cap??tulos publicados: ' +
                   (str(chap_tot) + '\n <br> \n'))
    htmlfile.write('Artigos completos publicados em peri??dicos: ' +
                   (str(acp_tot) + '\n <br> <br> \n'))
    htmlfile.write('Orienta????es:' + '\n <br>')
    if html_print_advi == 'NO':
        htmlfile.write('0' + '\n <br>')
    else:
        for oo in range(len(advi)):
            htmlfile.write(str(advi.iloc[oo, 0]).lower() +
                           ': ' + str(advi.iloc[oo, 1]) + '\n <br>')
    htmlfile.write('\n <hr> \n \n')
    # Projetos de Extensao do Grupo
    htmlfile.write('<a name="projexte"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de extens??o</h1> \n')
    if html_print_ppe_uniq == 'NO':
        htmlfile.write('N??o h?? projetos de extens??o <br>\n')
    else:
        htmlfile.write('<ol class="custom-counter">')
        for idd in range(len(dfppe_uniq_ext)):
            proj = dfppe_uniq_ext.iloc[idd, 0]
            proj_yi = dfppe_uniq_ext.iloc[idd, 1]
            proj_yf = dfppe_uniq_ext.iloc[idd, 2]
            proj_au = dfppe_uniq_ext.iloc[idd, 4]
            htmlfile.write('<li>' + '\n')
            htmlfile.write('<i>' + '\n')
            htmlfile.write('<u>' + str(proj) + '</u>. in??cio: <u>' +
                           str(proj_yi) + '</u>.' + ' fim: <u> ' + str(proj_yf)
                           + '.</u> ' + '<i>' + proj_au + '</i>.')
            htmlfile.write('\n </i>' + '\n')
            htmlfile.write('</li>' + '\n \n')
        htmlfile.write('</ol>')
    # Projetos de Pesquisa
    htmlfile.write('<a name="projpesq"></a>' + '\n \n')
    htmlfile.write('<h1>Projetos de pesquisa</h1> \n')
    if html_print_paper_all == 'NO':
        htmlfile.write('N??o h?? projetos de pesquisa <br>\n')
    else:
        htmlfile.write('<ol class="custom-counter">')
        for idd in range(len(dfppe_uniq_pesq)):
            proj = dfppe_uniq_pesq.iloc[idd, 0]
            proj_yi = dfppe_uniq_pesq.iloc[idd, 1]
            proj_yf = dfppe_uniq_pesq.iloc[idd, 2]
            proj_au = dfppe_uniq_pesq.iloc[idd, 4]
            htmlfile.write('<li>' + '\n')
            htmlfile.write('<i>' + '\n')
            htmlfile.write('<u>' + str(proj) + '</u>. in??cio: <u>' +
                           str(proj_yi) + '</u>' + ' fim: <u> ' + str(proj_yf)
                           + '.</u> ' + '<i>' + proj_au + '</i>.')
            htmlfile.write('\n </i>' + '\n')
            htmlfile.write('</li>' + '\n \n')
        htmlfile.write('</ol>')
    # Publicacao livros e capitulos
    htmlfile.write('<a name="pubbookchap"></a>' + '\n \n')
    htmlfile.write('<h1>Publica????o de livros e cap??tulos</h1> \n')
    if html_print_books_uniq == 'NO':
        htmlfile.write('N??o h?? livros publicados <br>\n')
    else:
        # Grafico de livros publicados por ano
        htmlfile.write('<h2>Produ????o de livros por ano</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/livros_dep_year.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write('<figcaption>N??mero de livros por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')
        # Grafico de capitulos publicados por ano
        htmlfile.write('<h2>Produ????o de cap??tulos por ano</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/capitulos_dep_year.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>N??mero de cap??tulos por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')
        # Resumo da producao de livros do GRUPO
        gg = dfbooks
        gg['YEAR'] = gg['YEAR'].apply(iint)
        gg = gg.groupby(['FULL_NAME', 'YEAR'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        gg.fillna(0, inplace=True)
        gg['TOTAL'] = gg.sum(axis=1)
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<h2> Resumo da produ????o de livros do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')

        if len(booknum99) >= 1:
            htmlfile.write('<b style="color:red;"> ATENCAO:\n ' + str(len(booknum99)) +
                           'projetos sem ano inicial</b>\n')
            for tt in range(len(booknum99)):
                htmlfile.write('\n <li>' + booknum99.iloc[tt, 0] + '\n </li>')
            htmlfile.write('<hr> \n')

    # Resumo da producao de capitulos do GRUPO
    if html_print_chapter_uniq == 'NO':
        htmlfile.write('N??o h?? cap??tulos publicados <br>\n')
    else:
        gg = dfchapters
        gg['YEAR'] = gg['YEAR'].apply(iint)
        gg = gg.groupby(['FULL_NAME', 'YEAR'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        gg.fillna(0, inplace=True)
        gg['TOTAL'] = gg.sum(axis=1)
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<h2> Resumo da produ????o de cap??tulos do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')

        if len(chapnum99) >= 1:
            htmlfile.write('<b style="color:red;"> ATENCAO:\n ' + str(len(chapnum99)) +
                           'projetos sem ano inicial</b>\n')
            for tt in range(len(chapnum99)):
                htmlfile.write('\n <li>' + chapnum99.iloc[tt, 0] + '\n </li>')
            htmlfile.write('<hr> \n')

    # Publicacao em periodicos
    htmlfile.write('<a name="pubperiod"></a>' + '\n \n')
    htmlfile.write('<h1>Publica????o em peri??dicos</h1> \n')
    if html_print_paper_uniq == 'NO':
        htmlfile.write('N??o h?? artigos em peri??dicos publicados <br>\n')
    else:
        # Grafico de producao de periodicos por ano
        htmlfile.write('<h2>Produ????o de peri??dicos por ano</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/period_dep_year.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>N??mero de publica????es por ano.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')
        # Grafico de producao por qualis
        htmlfile.write('<h2>Produ????o de peri??dicos por qualis</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/period_year_qualis.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Publica????es de peri??dicos por qualis.</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <hr> \n \n')

    # Grafico de interacao no grupos APENAS em artigos
    if html_print_paper_uniq == 'NO':
        htmlfile.write(
            'N??o foi possivel gerar intera????o entre pesquisadores <br>\n')
    else:
        htmlfile.write('<h2>Intera????o entre pesquisadores</h2> \n')
        htmlfile.write('<figure> \n')
        htmlfile.write('<img src="./figures/grapho.png" alt="" ')
        htmlfile.write('width = "560" height = "auto" >\n')
        htmlfile.write(
            '<figcaption>Grafo de colabora????o entre pesquisadores apenas em artigos</figcaption>\n')
        htmlfile.write('</figure> \n')
        htmlfile.write('\n <br> \n \n')
        # Lista de profissionais sem interacao em periodicos
        dfnointer_period = pd.read_csv('./csv_producao/periodicos_nointer.csv',
                                       sep=',', header=0)
        if len(dfnointer_period) > 0:
            htmlfile.write(
                '<b><i>N??o foi poss??vel localizar intera????es em peri??dicos para os seguintes pesquisadores: </i></b><br> \n')
            htmlfile.write('<ul>')
            for i in range(len(dfnointer_period)):
                name = dfnointer_period.iloc[i, 0]
                htmlfile.write('<b style="color:gray;"> <li>' +
                               name + '</li> </b> \n')
            htmlfile.write('\n </ul> \n <br> \n')
        htmlfile.write('\n <hr> \n \n')

    # lista de publicacoes em periodicos
    htmlfile.write('<h2>Rela????o de artigos em peri??dicos</h2> \n')
    htmlfile.write('<ol class="custom-counter">')
    for idd in range(len(dfpaper_uniq)):
        pap = dfpaper_uniq.iloc[idd, 0]
        pap_yi = dfpaper_uniq.iloc[idd, 1]
        pap_jo = dfpaper_uniq.iloc[idd, 4]
        pap_qu = dfpaper_uniq.iloc[idd, 5]
        pap_jc = round(float(dfpaper_uniq['JCR'].iloc[idd]), 1)
        pap_au = dfpaper_uniq['AUTHOR'].iloc[idd]
        htmlfile.write('<li>' + '\n')
        htmlfile.write('<i>' + '\n')
        htmlfile.write('<u>' + str(pap) + '</u>. ano: <u>' + str(pap_yi) + '</u>, ' +
                       str(pap_jo) + ', <b>' + str(pap_qu) + '</b>. ' +
                       ', <b>' + 'JCR ' + str(pap_jc) + '</b>. ' + str(pap_au))
        htmlfile.write('\n </i>' + '\n')
        htmlfile.write('</li>' + '\n \n')
    htmlfile.write('</ol> \n')
    # artig completo periodico por qualis para cada pesquisador
    htmlfile.write('<a name="prodporpesq"></a>' + '\n \n')
    htmlfile.write(
        '<h2>Produ????o individual de projetos e peri??dicos por ano e qualis ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n')
    for idd in range(len(dffullname)):
        # full name and link lattes
        htmlfile.write('<b><u>' + dffullname.iloc[idd, 1] + '</u></b> <br>')
        latteslink = 'http://lattes.cnpq.br/' + str(dffullname.iloc[idd, 0])
        htmlfile.write('- ' + '<a href="' + latteslink + '">' +
                       latteslink + '</a> ')
        lattesupda = str(dffullname.iloc[idd, 7])
        htmlfile.write('(atualizado em: ' +
                       lattesupda + ') <br> <br>')

        # ------------------------------------------------------------ ensino
        if html_print_ensidi == 'NO':
            htmlfile.write(
                'N??o disciplinas em ensino <br>\n')
        else:
            # disciplinas em ensino
            pp_idd = dfensidi[dfensidi['ID'] == str(
                dffullname.iloc[idd, 0])].reset_index(drop=True)
            pp_idd.drop(['ID', 'FULL_NAME', 'LAST_NAME',
                         'CITADO', 'CITY', 'STATE', 'RESUME',
                         'UPDATE', 'ADDRESS_ENTERP'],
                        axis=1, inplace=True)
            mm = (tabulate(pp_idd, headers="keys", tablefmt='html'))
            htmlfile.write('<b>Disciplinas em atividades de ensino</b><br>')
            htmlfile.write(str(mm))
        htmlfile.write('\n <br> \n')

        # ------------------------------------------------------------ okokok
        if html_print_ppe_all == 'NO':
            htmlfile.write(
                'N??o h?? projetos de pesquisa <br>\n')
        else:
            # projetos de pesquisa como coord
            pp_idd = dfppe_all[(dfppe_all['NATUREZA'] ==
                                'PESQUISA')].reset_index(drop=True)
            pp_idd = pp_idd[pp_idd['ID'] == str(
                dffullname.iloc[idd, 0])].reset_index(drop=True)
            # pp_idd = pp_idd[pp_idd['ID']
            #                 == str(1292986021348016)].reset_index(drop=True)
            count_pp_coord = 0
            lscount_pp_coord = []
            for ppi in range(len(pp_idd)):
                mm = pp_idd.iloc[ppi, 5]
                mm = mm.strip('[')
                mm = mm.strip(']')
                mm = mm.replace("'", "")
                mm = mm.split(',')
                mm = mm[0]
                mm = mm.strip()
                # print(mm)
                if mm == 'SIM':
                    count_pp_coord = count_pp_coord + 1
                    lscount_pp_coord.append(ppi)
            count_pp_integ = len(pp_idd) - count_pp_coord
            htmlfile.write('<b>Compila????o da produ????o</b><br>')
            htmlfile.write(
                '<li>' + 'total de projetos de pesquisa como coordenador = ' + str(count_pp_coord) + '</li>\n')
            # for ppii in range(len(lscount_pp_coord)):
            #     projname = pp_idd.iloc[lscount_pp_coord[ppii], 0]
            #     htmlfile.write('-' + str(projname + '\n <br> \n'))
            htmlfile.write(
                '<li>' + 'total de projetos de pesquisa como integrante = ' + str(count_pp_integ) + '</li>\n')
        # ------------------------------------------------------------
        # orientacoes
        if html_print_advi == 'NO':
            htmlfile.write('N??o h?? orientacoes <br>\n')
        else:
            t = dfadvise[dfadvise['ID'] == dffullname.iloc[idd, 0]]
            t = t.groupby(['NATURE'])['STUDENT'].size().reset_index()
            htmlfile.write('<li>Orienta????es: \n <br> \n ' + '</li>\n')
            for oo in range(len(t)):
                htmlfile.write(str(t.iloc[oo, 0]).lower() +
                               ' = ' + str(t.iloc[oo, 1]) + '\n <br>\n')
        # ------------------------------------------------------------
        # livros
        if html_print_books_all == 'NO':
            htmlfile.write('N??o h?? livros <br>\n')
        else:
            t = dfbooks[dfbooks['ID'] == dffullname.iloc[idd, 0]]
            t = t.groupby(['FULL_NAME', 'YEAR'])[
                'TITLE'].size().reset_index(drop=False)
            tot = t['TITLE'].sum()
            htmlfile.write('<li>produ????o total de livros = ' +
                           str(tot) + '</li>\n')
        # capitulos
        if html_print_chapter_all == 'NO':
            htmlfile.write('N??o h?? capitulos \n')
        else:
            t = dfchapters[dfchapters['ID'] == dffullname.iloc[idd, 0]]
            t = t.groupby(['FULL_NAME', 'YEAR'])[
                'TITLE'].size().reset_index(drop=False)
            tot = t['TITLE'].sum()
            # print(tot)
            htmlfile.write('<li>produ????o total de cap??tulos = ' +
                           str(tot) + '</li>\n')
        # artigos
        if html_print_paper_all == 'NO':
            htmlfile.write('N??o h?? publicacao em periodico \n')
        else:
            b = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
            b = b.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
                'TITLE'].size().unstack().reset_index(drop=False)
            b = b.fillna(0)
            b.drop('FULL_NAME', axis=1, inplace=True)
            t = dfpaper[dfpaper['ID'] == dffullname.iloc[idd, 0]]
            t = t.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
                'TITLE'].size().reset_index(drop=False)
            tot = t['TITLE'].sum()
            # print(tot)
            htmlfile.write('<li>produ????o total de artigos = ' +
                           str(tot) + '</li>\n <br> \n')
            # print(b.head())
            # print(tabulate(b.head(), headers="keys", tablefmt='markdown'))
            mm = (tabulate(b, headers="keys", tablefmt='html'))
            htmlfile.write(str(mm))
        htmlfile.write('\n <hr> \n')
        # ------------------------------------------------------------

    # ------------------------------------------------------------
    # Tabela de orientacoes
    if html_print_advi == 'NO':
        htmlfile.write('N??o h?? orientacoes <br>\n')
    else:
        advgg = dfadvise
        advgg['NATURE'] = advgg['NATURE'].str.replace('-', ' ')
        advgg['NATURE'] = advgg['NATURE'].str.replace('_', ' ')
        advgg = advgg.groupby(['FULL_NAME', 'NATURE'])[
            'STUDENT'].size().unstack().reset_index(drop=False)
        advgg.fillna(0, inplace=True)
        advgg['TOTAL'] = advgg.sum(axis=1)
        advggt = (tabulate(advgg, headers="keys", tablefmt='html'))
        htmlfile.write(
            '<h2> Resumo de orienta????es do grupo ' + str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
        htmlfile.write(advggt + ' \n')
        htmlfile.write(
            '<i>Possibilidade da contabiliza????o de co-orienta????o.</i>')

    # ------------------------------------------------------------
    # Tabela de producao em periodicos
    if html_print_paper_all == 'NO':
        htmlfile.write('N??o h?? publicacao em peri??dico <br>\n')
    else:
        gg = dfpaper
        gg = gg.groupby(['FULL_NAME', 'QUALIS'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        gg.fillna(0, inplace=True)
        gg['TOTAL'] = gg.sum(axis=1)
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<h2> Resumo da produ????o de artigos em peri??dicos do grupo ' +
            str(int(yyi)) + '-' + str(int(yyf)) + '</h2> \n <br> \n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')

        if len(ppenum99) >= 1:
            htmlfile.write('<b style="color:red;"> ATENCAO:\n ' +
                           str(len(ppenum99)) +
                           'projetos sem ano inicial</b>\n')
            for tt in range(len(ppenum99)):
                htmlfile.write('\n <li>' + ppenum99.iloc[tt, 0] + '\n </li>')
            htmlfile.write('<hr> \n')
        if len(pernum99) >= 1:
            htmlfile.write('<b style="color:red;"> ATENCAO:\n ' +
                           str(len(pernum99)) +
                           'peri??dicos sem ano</b>\n')
            for tt in range(len(pernum99)):
                htmlfile.write('\n <li>' + pernum99.iloc[tt, 0] + '\n </li>')
            htmlfile.write('<hr> \n')

    # ------------------------------------------------------------
    # Tabela de indicadores qualis
    # ------------------------------------------------------------
    htmlfile.write('<a name="indcapes"></a>' + '\n \n')
    htmlfile.write('<h1 class="title">Indicadores CAPES</h1> \n')
    # ------------------------------------------------------------
    ls_ppgs = fun_ppgs()
    name_ppg = fun_nomeppg()
    htmlfile.write(
        'Para saber o m??todo de c??lculo dos ??ndices consulte <a href="https://rafatieppo.github.io/lucylattes/">https://rafatieppo.github.io/lucylattes/</a>' + '.<br>' + '\n \n')
    htmlfile.write(
        'Os seguintes PPGs foram econtrados nos curriculos dos pesquisadores: ' + str(ls_ppgs) + '.<br>' + '\n \n')
    htmlfile.write('O PPG avaliado foi: <b>' +
                   str(name_ppg) + '</b><br>\n')
    # ------------------------------------------------------------
    # Indicador qualis indori
    if html_print_indori == 'NO':
        htmlfile.write(
            'N??o h?? indicador capes de ??ndice de orienta????o do grupo <br>\n')
    else:
        gg = dfind_capes_indori
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        htmlfile.write(
            '<h2> ??ndice de orienta????o (IndOri)' + '</h2> \n <br> \n')
        htmlfile.write('<p> Avalia as defesas com orienta????o de docentes permanentes(DP) do programa. O indicador ?? calculado para cada ano e depois calculada a m??dia para o quadri??nio </p>\n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')
        htmlfile.write('<p><i> Para que a orienta????o possa ser contabiliza, no cadastro de orienta????es do curr??culo Lattes do pesquisador, o nome do PPG da orienta????o deve ser id??ntico ao PPG avaliado. Ma??sculas e min??sculas N??O diferem. </i></p><br><br>\n')
    # ------------------------------------------------------------
    # Indicador qualis indprodart
    if html_print_indori == 'NO':
        htmlfile.write(
            'N??o h?? indicador capes de ??ndice de produ????o de artigo do grupo<br>\n')
    else:
        gg = dfind_capes_indprodart
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write('<h2> ??ndice de Produtividade referente a artigos ' +
                       'cient??ficos (IndProdArt)' + '</h2> \n <br> \n')
        htmlfile.write('<p> Avalia toda a produ????o intelectual do programa no formato de artigo cient??fico, sendo que a participa????o de um docente permanente como autor ?? condi????o obrigat??ria para validar a produ????o. </p>\n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')

    # ------------------------------------------------------------
    # Indicador qualis indautdis
    if html_print_indautdis == 'NO':
        htmlfile.write(
            'N??o h?? indicador capes de ??ndice de produ????o de artigo do grupo<br>\n')
    else:
        gg = dfind_capes_indautdis
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<h2> ??ndice de autoria discente' + '</h2> \n <br> \n')
        htmlfile.write('<p>??ndice de discentes autores (IndAut):Avalia a propor????o de discentes autores (E) em rela????o ao total de discentes do programa. Foram considerados para o c??lculo de E, os discentes e egressos at?? cinco anos quando autores de artigos. </p>\n')
        htmlfile.write('<p>??ndice de produtos com autoria discente (IndDis): Avalia a quantidade de produtos intelectuais (artigos) de autoria discente ou de egressos at?? 5 anos, em rela????o ao total de discentes do programa (G).  </p>\n')
        htmlfile.write(
            '<i>Considera apenas produ????o em peri??dicos </i><br><br>\n')
        htmlfile.write(ggt + '\n <br> \n <br> \n')
        htmlfile.write(
            '<i>INDAUT: ??ndice de discentes autores, INDDIS: ??ndice de produtos com autoria discente</i>')

    # ------------------------------------------------------------
    # Indicador qualis distindproddp
    if html_print_distindproddp == 'NO':
        htmlfile.write(
            'N??o h?? indicador capes de Ind. de distrib. dos docentes permanentes por faixa de IndProd <br>\n')
    else:
        gg = dfind_capes_distindproddp
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<h2> Indicador de distribui????o dos docentes permanentes por faixa de IndProd (DistIndProdDP)' + '</h2> \n <br> \n')
        htmlfile.write('<p>Nesse caso, calcula-se o IndProd para cada docente permanente e posteriormente os docentes s??o distribu??dos conforme as faixas apresentadas para o IndProd. Feito isso, calcula-se o percentual de docentes permanentes (DP) classificados em cada faixa (MB, B, R e F/D) em rela????o ao corpo docente permanente total. O somat??rio dos percentuais das faixas MB, B e R permite avaliar o equil??brio na distribui????o da produ????o docente. </p>\n')
        htmlfile.write(
            '<i>Classifica????o dos pesquisadores por quadri??nio</i><br><br>')
        htmlfile.write(ggt + '\n <br> \n <br> \n')
        # imprimir tabela com resultuda do grupo
        dfind_capes_distindproddp = pd.read_csv('./csv_producao/capesindex_distindproddp.csv',
                                                header=0, dtype='str')
        gg = dfind_capes_distindproddp
        ggt = (tabulate(gg, headers="keys", tablefmt='html'))
        # print(ggt)
        htmlfile.write(
            '<i>Indicador DistIndProdDP</i><br><br>')
        htmlfile.write(ggt + '\n <br> \n <br> \n')

        htmlfile.write('<hr> \n')

    # ------------------------------------------------------------
    # Gostou?
    htmlfile.write('<b>GOSTOU ?</b>\n')
    htmlfile.write(
        '<li>Acesse <a href="https://github.com/rafatieppo/lucyLattes">reposit??rio lucyLattes</a> ' +
        'e nos de uma estrela clicando na estrela no topo da p??gina(lado direito)</li>\n')
    htmlfile.write('<ul> \n')
    htmlfile.write(
        '<li> Caso queira, vc pode pode ajudar com quanto quiser para manter o projeto via PayPal:  </li>\n')
    htmlfile.write('<a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=68LAA9FZLABUQ" > <img border="0" alt="" src="https://sites.google.com/site/zownloads/home/gifs/logo_rt_donate.png" width="150"> </a>\n <br> <br>\n')
    htmlfile.write(
        '<br> \n')
    htmlfile.write('<b>AVISOS</b>:\n ')
    htmlfile.write(
        '<li>Arquivo para classificacao qualis utilizado: <code>' + qualqualis + '</code >')
    htmlfile.write('<li>Este programa ?? um software livre; voc?? pode redistribui-lo e/ou modifica-lo dentro dos termos da Licen??a P??blica Geral GNU. Verifique o arquivo LICENSE.txt</li> \n')
    htmlfile.write(
        '<li>Os resultados est??o sujeitos a falhas devido a inconsistencias no preenchimento dos CVs Lattes</li>\n')
    htmlfile.write(
        '<li>Em caso de erro do script abra um chamado no <a href="https://github.com/rafatieppo/lucyLattes">reposit??rio lucyLattes</a>  </li>\n')
    htmlfile.write(
        '<li>O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta relatorio</li>\n')
    htmlfile.write(
        '<li>O arquivo relatorio_producao.html foi gerado na pasta relatorio</li>\n')
    htmlfile.write(
        '<li>Caso precise citar ?? poss??vel usar o DOI: 10.5281/zenodo.2591748</li>\n')
    htmlfile.write('<br> <br> <br>')
    htmlfile.write('<footer> \n')
    htmlfile.write(
        'Relat??rio gerado por lucyLattes v1.1 Os resultados est??o sujeitos a falhas devido a inconsist??ncias no preenchimento dos CVs Lattes.')
    htmlfile.write('\n <br>')
    htmlfile.write('Para maiores informa????es acesse: ')
    htmlfile.write(
        '<a href="https://rafatieppo.github.io/lucylattes/">https://rafatieppo.github.io/lucylattes/</a> \n <br> \n')
    htmlfile.write('</footer> \n')
    htmlfile.close()
    # ------------------------------------------------------------
    # arquivo csv com autores producao ano qualis
    if html_print_paper_all == 'NO':
        print('Relatorio autor qualis miss')
    else:
        acpq_pesq = dfpaper_uniq.groupby(['FULL_NAME', 'YEAR', 'QUALIS'])[
            'TITLE'].size().unstack().reset_index(drop=False)
        acpq_pesq = acpq_pesq.fillna(0)
        acpq_pesq.to_csv('./relatorio/extrato_periodico_autorqualis.csv')
    print('------------------------------------------------------------')
    print('AVISOS')
    print('------------------------------------------------------------')
    print('- Arquivo para classificacao qualis utilizado: ' + qualqualis)
    print('- Este programa ?? um software livre; voc?? pode redistribui-lo e/ou modifica-lo dentro dos termos da Licen??a P??blica Geral GNU. Verifique o arquivo LICENSE.txt ')
    print('- Os resultados est??o sujeitos a falhas devido a inconsistencias no preenchimento dos CVs Lattes')
    print('- Em caso de erro do script abra um chamado em https://github.com/rafatieppo/lucyLattes')
    print('- O arquivo extrato_periodico_autorqualis.csv foi gerado na pasta relatorio')
    print('- O arquivo relatorio_producao.html foi gerado na pasta relatorio')
    print('- Caso precise citar ?? poss??vel usar o DOI: 10.5281/zenodo.2591748')
    print('------------------------------------------------------------')

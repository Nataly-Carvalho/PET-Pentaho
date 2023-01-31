#!/usr/bin/python3
# -*- coding: utf-8 -*-
import platform
import re
import glob
import os
import pandas as pd
import numpy as np
from extrafuns import *

# ------------------------------------------------------------
# packages
# ------------------------------------------------------------
# ------------------------------------------------------------

# ------------------------------------------------------------
# Funcoes
# ------------------------------------------------------------


def gettidydf():
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
    # verificando sistema
    plat_sys = platform.system()
    # ------------------------------------------------------------
    # Projetos de pesquisa e extensão
    # ------------------------------------------------------------
    # df com todos os projetos pesq e ext
    lscsv_ppe = glob.glob('./csv_producao/*_ppe.csv')
    dfppe = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_ppe)):
        a = pd.read_csv(lscsv_ppe[i], header=0)
        dfppe = dfppe.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_ppe, i)
        #iid = str(lscsv_ppe[i].split('_')[1].split('/')[1])
        idrep = np.repeat(iid, len(a['PROJ']))
        lsid.append(idrep)
    dfppe['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    # df com nome completo, sobrenome e iid
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
        # passando ID para string, para poder comparar com dfpaper
        # cancelei a ss() pq o read_csv do a esta com dtype='str
    dffullname['ID'] = dffullname['ID'].apply(ss)
    dffullname.to_csv('./csv_producao/fullname_all.csv',
                      sep=',', index=False)
    dfppe = pd.merge(dfppe, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PROJETOS repetido busca o sobrenome do autor no
    # dffullname por meio do iid lattes. divide a coluna autores do
    # paper. verifica a ordem do sobrenome no author_split
    lsauthor_order = []
    order = -99
    for i in range(len(dfppe['ID'])):
        lastname = dffullname[dffullname['ID']
                              == (dfppe.iloc[i, 6])]
        lastname = lastname.iloc[0, 2]
        author_split = dfppe.iloc[i, 7].split(',')
        # print(lastname)
        # print(len(author_split))
        for aa in range(len(author_split)):
            test = lastname in author_split[aa]
            if test == True:
                order = aa + 1
        lsauthor_order.append(order)
    dfppe['OR'] = lsauthor_order
    # retirando projeto repetido, fica para o author com maior importancia
    dfppe_uniq = dfppe.sort_values(['OR'])
    dfppe_uniq.drop_duplicates(['PROJ'], inplace=True)
    pathfilename = str('./csv_producao/projetos_all.csv')
    dfppe.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfppe['PROJ']), ' projetos')
    pathfilename = str('./csv_producao/projetos_uniq.csv')
    dfppe_uniq.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfppe_uniq['PROJ']), ' projetos')

    # ------------------------------------------------------------
    # Producao bibliografica
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_paper = glob.glob('./csv_producao/*period.csv')
    dfpaper = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_paper)):
        a = pd.read_csv(lscsv_paper[i], header=0)
        dfpaper = dfpaper.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_paper, i)
        # iid = str(lscsv_paper[i].split('_')[1].split('/')[1])
        idrep = np.repeat(iid, len(a['TITLE']))
        lsid.append(idrep)
    dfpaper['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    # df com nome completo, sobrenome e iid
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    # passando IID para string, para poder comparar com dfpaper
    # cancelei a ss() pq o read_csv do a esta com dtype='str
    # dffullname['ID'] = dffullname['ID'].apply(ss)
    dfpaper = pd.merge(dfpaper, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    # processo para excluir PAPER repetido busca o sobrenome do autor no
    # dffullname por meio do iid lattes. divide a coluna autores do
    # paper.
    # atual: a ordem já vem no dfpaper
    # antiga: verifica a ordem do sobrenome no author_split
    #lsauthor_order = []
    #order = -99
    # for i in range(len(dfpaper['ID'])):
    #     lastname = dffullname[dffullname['ID']
    #                           == (dfpaper.iloc[i, 9])]
    #     lastname = lastname.iloc[0, 2]
    #     author_split = dfpaper.iloc[i, 7].split(',')
    #     # print(lastname)
    #     # print(len(author_split))
    #     for aa in range(len(author_split)):
    #         test = lastname in author_split[aa]
    #         if test == True:
    #             order = aa + 1
    #     lsauthor_order.append(order)
    #dfpaper['OR'] = lsauthor_order
    # retirando paper repetido, fica para o author com maior importancia
    dfpaper_uniq = dfpaper.sort_values(['ORDER_OK'])
    dfpaper_uniq.drop_duplicates(['TITLE'], inplace=True)
    pathfilename = str('./csv_producao/periodicos_all.csv')
    dfpaper.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper['TITLE']), ' artigos')
    pathfilename = str('./csv_producao/periodicos_uniq.csv')
    dfpaper_uniq.to_csv(pathfilename, index=False)
    print(pathfilename, ' gravado com',
          len(dfpaper_uniq['TITLE']), ' artigos')

    # ------------------------------------------------------------
    # Producao bibliografica LIVROS
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_book = glob.glob('./csv_producao/*livro.csv')
    if len(lscsv_book) < 1:
        print('Producao de livros nao encontrada')
    else:
        dfbook = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_book)):
            a = pd.read_csv(lscsv_book[i], header=0)
            dfbook = dfbook.append(a, ignore_index=False)
            iid = fun_idd_unixwind(plat_sys, lscsv_book, i)
            # iid = str(lscsv_book[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['TITLE']))
            lsid.append(idrep)
        dfbook['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
            # passando IID para string, para poder comparar com dfbook
            # cancelei a ss() pq o read_csv do a esta com dtype='str
            # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfbook = pd.merge(dfbook, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        dfbook_uniq = dfbook.sort_values(['ORDER_OK'])
        dfbook_uniq.drop_duplicates(['TITLE'], inplace=True)
        pathfilename = str('./csv_producao/livros_all.csv')
        dfbook.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfbook['TITLE']), ' livros')
        pathfilename = str('./csv_producao/livros_uniq.csv')
        dfbook_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfbook_uniq['TITLE']), ' livros')

    # ------------------------------------------------------------
    # Producao bibliografica CAPITULOS
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_chapter = glob.glob('./csv_producao/*capitulo.csv')
    if len(lscsv_chapter) < 1:
        print('Producao de capitulos nao encontrada')
    else:
        dfchapter = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_chapter)):
            a = pd.read_csv(lscsv_chapter[i], header=0)
            dfchapter = dfchapter.append(a, ignore_index=False)
            iid = fun_idd_unixwind(plat_sys, lscsv_chapter, i)
            # iid = str(lscsv_chapter[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['TITLE']))
            lsid.append(idrep)
        dfchapter['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
        # passando IID para string, para poder comparar com dfchapter
        # cancelei a ss() pq o read_csv do a esta com dtype='str
        # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfchapter = pd.merge(dfchapter, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        dfchapter_uniq = dfchapter.sort_values(['ORDER_OK'])
        dfchapter_uniq.drop_duplicates(['TITLE'], inplace=True)
        pathfilename = str('./csv_producao/capitulos_all.csv')
        dfchapter.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfchapter['TITLE']), ' capitulos de livros')
        pathfilename = str('./csv_producao/capitulos_uniq.csv')
        dfchapter_uniq.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfchapter_uniq['TITLE']), ' capitulos de livros')

    # ------------------------------------------------------------
    # ORIENTACAO TCC IC MESTRADO DOUTORADO
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_advi = glob.glob('./csv_producao/*advis.csv')
    if len(lscsv_advi) < 1:
        print('Orientacao para TCC, IC, MESTRADO ou DOUTORADO nao encontrada')
    else:
        dfadvi = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_advi)):
            a = pd.read_csv(lscsv_advi[i], header=0)
            dfadvi = dfadvi.append(a, ignore_index=False)
            iid = fun_idd_unixwind(plat_sys, lscsv_advi, i)
            # iid = str(lscsv_advi[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['YEAR']))
            lsid.append(idrep)
        dfadvi['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        # len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
            # passando IID para string, para poder comparar com dfadvi
            # cancelei a ss() pq o read_csv do a esta com dtype='str
            # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfadvi = pd.merge(dfadvi, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        pathfilename = str('./csv_producao/orientacoes_all.csv')
        dfadvi.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfadvi['YEAR']), ' orientacoes')

    # ------------------------------------------------------------
    # ENSINO DISCIPLINAS
    # ------------------------------------------------------------
    # df com todos os periodicos
    lscsv_ensdisc = glob.glob('./csv_producao/*ensdisc.csv')
    if len(lscsv_ensdisc) < 1:
        print('Disciplinas para ensino nao encontrada')
    else:
        dfensdis = pd.DataFrame()
        lsid = []
        for i in range(len(lscsv_ensdisc)):
            a = pd.read_csv(lscsv_ensdisc[i], header=0)
            dfensdis = dfensdis.append(a, ignore_index=False)
            iid = fun_idd_unixwind(plat_sys, lscsv_ensdisc, i)
            # iid = str(lscsv_ensdisc[i].split('_')[1].split('/')[1])
            idrep = np.repeat(iid, len(a['YEAR_INI']))
            lsid.append(idrep)
        dfensdis['ID'] = np.concatenate(lsid)
        lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
        # len(lscsv_fullname)
        # df com nome completo, sobrenome e iid
        dffullname = pd.DataFrame()
        for i in range(len(lscsv_fullname)):
            a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
            dffullname = dffullname.append(a, ignore_index=False)
            # passando IID para string, para poder comparar com dfensdis
            # cancelei a ss() pq o read_csv do a esta com dtype='str
            # dffullname['ID'] = dffullname['ID'].apply(ss)
        dfensdis = pd.merge(dfensdis, dffullname, on='ID')
        dffullname = dffullname.reset_index(drop=True)
        pathfilename = str('./csv_producao/ensdisc_all.csv')
        dfensdis.to_csv(pathfilename, index=False)
        print(pathfilename, ' gravado com',
              len(dfensdis['YEAR_INI']), ' periodos de disciplinas')

    #################################################
    #---------------LINHAS DE PESQUISA--------------#
    #################################################

    lscsv_ldp = glob.glob('./csv_producao/*_ldp.csv')
    dfldp = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_ldp)):
        a = pd.read_csv(lscsv_ldp[i], header=0)
        dfldp = dfldp.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_ldp, i)
        idrep = np.repeat(iid, len(a['PESQUISA']))
        lsid.append(idrep)
    dfldp['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfldp = pd.merge(dfldp, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/linhas_de_pesquisa_all.csv')
    dfldp.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravado com', len(dfldp['PESQUISA']), 'linhas de pesquisa')

    ##################################################
    #---------------PREMIOS OU TITULOS --------------#
    ##################################################

    lscsv_pt = glob.glob('./csv_producao/*_pt.csv')
    dfpt = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_pt)):
        a = pd.read_csv(lscsv_pt[i], header=0)
        dfpt = dfpt.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_pt, i)
        idrep = np.repeat(iid, len(a['TITULO']))
        lsid.append(idrep)
    dfpt['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfpt = pd.merge(dfpt, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/premios_ou_titulos_all.csv')
    dfpt.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravado com', len(dfpt['TITULO']), ' premios e titulos')

    ##################################################
    # ----------------- PRODUÇÕES -------------------#
    ##################################################

    lscsv_prods = glob.glob('./csv_producao/*_prods.csv')
    dfprods = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_prods)):
        a = pd.read_csv(lscsv_prods[i], header=0)
        dfprods = dfprods.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_prods, i)
        idrep = np.repeat(iid, len(a['TITULO']))
        lsid.append(idrep)
    dfprods['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfprods = pd.merge(dfprods, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/producoes_all.csv')
    dfprods.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravado com', len(dfprods['TITULO']), 'producoes de CT')

    ##################################################
    # ---------------PROJETOS DE ENSINO--------------#
    ##################################################

    lscsv_pen = glob.glob('./csv_producao/*_proj_ens.csv')
    dfpen = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_pen)):
        a = pd.read_csv(lscsv_pen[i], header=0)
        dfpen = dfpen.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_pen, i)
        idrep = np.repeat(iid, len(a['PROJETO']))
        lsid.append(idrep)
    dfpen['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfpen = pd.merge(dfpen, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/projetos_ensino_all.csv')
    dfpen.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravado com', len(dfpen['PROJETO']), 'projetos de ensino')

    ######################################################
    # ---------------CURSO DE CURTA DURAÇÃO--------------#
    ######################################################

    lscsv_cdd = glob.glob('./csv_producao/*_ccd.csv')
    dfccd = pd.DataFrame()
    lsid = []
    for i in range(len(lscsv_cdd)):
        a = pd.read_csv(lscsv_cdd[i], header=0)
        dfccd = dfccd.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_cdd, i)
        idrep = np.repeat(iid, len(a['COURSE']))
        lsid.append(idrep)
    dfccd['ID'] = np.concatenate(lsid)
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfccd = pd.merge(dfccd, dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/cursos_de_curta_duracao_all.csv')
    dfccd.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravadp com', len(dfccd['COURSE']), 'cursos de curta duracao')

    ##############################################################
    #-------------------------Patentes---------------------------#
    ##############################################################

    lscsv_patente = glob.glob('./csv_producao/*_patentes.csv')
    dfpatente  = pd.DataFrame()
    lsid = []
    lssid = []
    for i in range(len(lscsv_patente)):
        a = pd.read_csv(lscsv_patente[i], header=0)
        dfpatente = dfpatente.append(a, ignore_index=False)
        iid = fun_idd_unixwind(plat_sys, lscsv_patente, i)
        idrep = np.repeat(iid, len(a['TITULO']))
        lsid.append(idrep)
    dfpatente['ID'] = np.concatenate(lsid)
    lscsv_nomes_autores = glob.glob('./csv_producao/*_autores_pat.csv')
    len(lscsv_nomes_autores)
    dfnomesautores = pd.DataFrame()
    #for i in range(len(lscsv_nomes_autores)):
    #    a = pd.read_csv(lscsv_nomes_autores[i], header=0, dtype='str')
    #    dfnomesautores = dfnomesautores.append(a, ignore_index=False)
    #    iiid = fun_idd_unixwind(plat_sys, lscsv_nomes_autores, i)
    #    idrep = np.repeat(iiid, len(a['COD_PATENTE_AUTORIA']))
    #    lssid.append(idrep)
    #dfnomesautores['ID'] = np.concatenate(lssid)
    #dfpatente = pd.merge(dfpatente, dfnomesautores, on='ID')
    lscsv_fullname = glob.glob('./csv_producao/*fullname.csv')
    len(lscsv_fullname)
    dffullname = pd.DataFrame()
    for i in range(len(lscsv_fullname)):
        a = pd.read_csv(lscsv_fullname[i], header=0, dtype='str')
        dffullname = dffullname.append(a, ignore_index=False)
    dfpatente = pd.merge(dfpatente,dffullname, on='ID')
    dffullname = dffullname.reset_index(drop=True)
    pathfilename = str('./csv_producao/patentes_all.csv')
    dfpatente.to_csv(pathfilename, index=False)
    print(pathfilename, 'gravado com', len(dfpatente['TITULO']), 'patentes')






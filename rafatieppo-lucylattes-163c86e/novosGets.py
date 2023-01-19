def getpremio(zipname):
    zipfilepath = './xml_zip' + '/'+ str(zipname)
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
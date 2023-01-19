def getpremio(zipname):
    zipfilepath = './xml_zip' + '/'+ str(zipname)
    archive = zipfile.ZipFile(zipfilepath, 'r')
    lattesxmldata = archive.open('curriculo.xml')
    soup = BeautifulSoup (lattesxmldata, 'lxml', from_encoding= 'ISO-8859-1')
    pts = soup.find_all ('premios-titulo')

    if len(pts) == 0:
        print('Demais premios e titulos não encontrado para: ', zipname)
    else:
        ls_pt_name = []
        ls_pt_entpromot = []
        ls_pt_year = []
        ls_pt_name_i =[]
        for i in range(len(pts)):
            pt = pts[i].find_all('premio-titulo')
            if len(pt) == 0:
                print('Premios e titulos não encontrado para', zipname)
            else:
                for j in range (len(pt)):
                    titulo = str(pt[j])
                    result = re.search('nome-do-premio-ou-titulo\"(.*)\" nome-da-entidade-promotora', titulo_premio)
                    cc = fun_result(result)
                    ls_pt_name.append(cc)

                    titulo_premio = str(pt[j])
                    result = re.search('ano-da-premiacao=\"(.*)\" nome-do-premio-ou-titulo-ingles', titulo_premio)
                    cc = fun_result(result)
                    ls_pt_year.append(cc)
                    entpromot = pt[j].find_all('entidade-promotora')
                    ls_all_premios_titulo = []

                    for k in range (len(entpromot)):
                        entpromot = str(entpromot[k])
                        result = re.search('nome-da-entidade-promotora')
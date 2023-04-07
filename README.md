## PET-Pentaho
### Projeto desenvolvido para o PET-Facep com parceria com o CESAR School
Orientadores: Rafael Ferreira e Luana Cristina 

ANÁLISE DOS DADOS
Fonte dos dados: O projeto se trata de extrair dados de currículos de pesquisadores do Cesar na plataforma https://lattes.cnpq.br  utilizado o LucyLates com base no repositório  https://github.com/rafatieppo/lucylattes para automatizar o processo (O LucyLattes é programado em python), os dados que precisamos extrair foram os seguintes.

- Atuação profissional
- Linhas de pesquisa
- Projetos de pesquisa
- Projetos de extensão
- Projetos de ensino
- Projetos de desenvolvimento
- Prêmios e títulos
- Produções
- Patentes e registros
- Bancas
- Orientações
<br>
Alguns dos arquivos já estavam disponíveis por padrão do lucyLattes, mas foi necessário implementar algumas funções para conseguir pegar os dados acima.

- O que foi feito para a extração dos dados pelo lucyLattes, primeiramente é necessário baixar o Lucylattes e por padrão vai vir uma pasta chamada xml_zip que se encontra na pasta rafatieppo-lucylattes-163c86e.
<br>
<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/FLRjyeN.png" title="source: imgur.com" /></a>
<br>
no https://lattes.cnpq.br baixe os curriculum e em seguida deve ser colocado na pasta xml_zip ainda zipado.
- Volte para outra pasta e encontre a pasta list_id_name.txt.
<br>
<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/egjnOdK.png" title="source: imgur.com" /></a>
<br>
E adicione ID do pesquisador que é o nome da pasta quando é baixado Lattes o nome e o título da pessoa.
<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/mFTfVKF.png" title="source: imgur.com" /></a>

## Python 
- O código no python foi feito com base nos outros códigos que estavam por padrão no lucylattes se encontra no arquivo scraperlattes.py
<br>
- Ex: Banca de TCC
<br>
<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/LVsJ0W5.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/jyIEPZg.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/NsfsO4O.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/mnNnzlY.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/oQFQgGX.png" title="source: imgur.com" /></a>
<br>
- Após o código ser rodado é gerado  arquivos csv de cada pesquisador e os merges,os merges estão no arquivo tidydf.py
- Ex: Merge Banca de Graduação
<br>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/E1ERqM0.png" title="source: imgur.com" /></a>
<br>
- No merge é feito a junção das tabelas escolhidas e com a tabela full name.
<br>

- E então foi chamada no LucyLattes.py
<br>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/vE2svaf.png" title="source: imgur.com" /></a>
<br>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/Vd8GWyu.png" title="source: imgur.com" /></a>


## Pentaho
- Foi feito o tratamento de dados utilizando o pentaho padronizando todos os arquivos e conectando eles com o banco de dados (PostgresSQL), todos os arquivos foram colocados em caixa alta e foram retirados os acentos.
- O formato da fonte externa é .csv e está sendo separado por vírgula(,).
<br>


<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/NZ1t2nY.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/dttviKf.png" title="source: imgur.com" /></a>


↬→→→→→→→→→→→→→→→→→→→→→→→→→•••••←←←←←←←←←←←←←←←←←←←←←←←←←←←←↫

Apos isso foi realizado um dump com a database gerando o arquivo stage_pesq.sql usando o seguinte com:

pg_dump -h localhost -p 5432 -U postgres stage_pesq > C:\stage_pesq.sql

e para acessar as tabelas usa o comando:

psql -h nomeservidor -U nomeusuario -d nomebancodedados < /caminho/nomearquivo.sql

↬→→→→→→→→→→→→→→→→→→→→→→→→→•••••←←←←←←←←←←←←←←←←←←←←←←←←←←←←↫
# Metabase
<br>
O metabase foi utilizado para a visualização 
O Metabase é uma ferramenta de análise e visualização de dados gratuita e de código aberto que permite conectar e consultar diversas fontes de dados e criar painéis interativos. Para começar a usá-lo, siga estes passos:
Baixe e instale o Metabase:
- Acesse o site oficial do Metabase (https://www.metabase.com/) e clique em "Download" no menu superior.
<img align="center"   src="https://i.imgur.com/15owhLS.png" title="source: imgur.com"/>
<img align="center"  src="https://i.imgur.com/UJrdK9o.png" title="source: imgur.com"/>


- Escolha a opção que corresponde ao seu sistema operacional e siga as instruções de instalação.
- Conecte-se a uma fonte de dados:
- Abra o Metabase e clique em "Add a database" para adicionar uma fonte de dados.
- Escolha a opção que corresponde ao tipo de banco de dados que você quer conectar e siga as instruções para preencher as informações de conexão.
<br>
     
Após preencher as informações de conexão, clique em "Save" para salvar as configurações.
Crie uma pergunta:
- Clique em "Perguntar" para criar uma nova pergunta.
<img align="center" src="https://i.imgur.com/l5pYqTx.png" title="source: imgur.com"/>

- Escolha a fonte de dados que você quer usar na pergunta.
<img align="center" src="https://i.imgur.com/NmNGlSO.png" title="source: imgur.com"/>

- Selecione as tabelas e campos que você quer incluir na pergunta.
<img align="center"  src="https://i.imgur.com/svlgDy1.png" title="source: imgur.com"/>

- Escolha a forma de visualização que você quer usar para exibir os dados.
<img align="center"  src="https://i.imgur.com/2BNTrrU.png" title="source: imgur.com"/>

- Clique em "Feito" para ver os resultados da pergunta.
<img align="center"   src="https://i.imgur.com/lZ0G87r.png" title="source: imgur.com"/>

- E logo após salve e adicione no painel de sua preferência
<img align="center" src="https://i.imgur.com/3CVbe3f.png" title="source: imgur.com"/>




Tecnologias usadas:

<div style="display: inline_block"><br>
<img align="center"  height="100" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/>
-
<img align="center"  height="150" width="150" src="https://i.imgur.com/Ko865kR.png" title="source: imgur.com"/>
- 
<img align="center"  height="90" width="150" src="https://i.imgur.com/rq6vHFU.png" title="source: imgur.com"/>


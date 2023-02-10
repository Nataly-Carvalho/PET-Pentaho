## PET-Pentaho
### Projeto desenvolvido para o PET-Facep com parceria com o CESAR School
Orientadores: Rafael Ferreira e Luana Cristina 

O projeto se trata de extrair dados de curriculos de pesquisadores da <a href="https://lattes.cnpq.br"> Plataforma Lattes</a> ultilizado o <a href="https://github.com/rafatieppo/lucylattes">lucyLattes</a> para automatizar o processo (O lucyLattes é programado em python), os dados que precisamos extrair foram os seguintes

- Atuação profissional
- Linhas de pesquisa 
- Projetos de pesquisa 
- Projetos de extensão 
- Projetos de ensino
- Projetos de desenvolvimento
- Premios e titulos 
- Produções
- Patentes e registros
- Bancas 
- Orientações 

Alguns dos arquivos ja estava disponiveis por padrão do lucyLattes mais foi nescessario implementar algumas funções para conseguir pegar os dados acima.

↬→→→→→→→→→→→→→→→→→→→→→→→→→•••••←←←←←←←←←←←←←←←←←←←←←←←←←←←←↫

Logo apos foi feito o tratamento de dados utilizando o pentaho padronizando todos os arquivos e conectando eles com o banco de dados (PostgresSQL), todos os arquivos foram colocados em caixa alta e foram retirados os acentos.

<a href="https://imgur.com/p9vLtvR"><img src="https://i.imgur.com/p9vLtvR.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/fSzYVgg"><img src="https://i.imgur.com/fSzYVgg.png" title="source: imgur.com" /></a>
<a href="https://imgur.com/BJUq3Lw"><img src="https://i.imgur.com/BJUq3Lw.png" title="source: imgur.com" /></a>

↬→→→→→→→→→→→→→→→→→→→→→→→→→•••••←←←←←←←←←←←←←←←←←←←←←←←←←←←←↫

Apois isso foi realizado um dump com a database gerando o arquivo stage_pesq.sql usando o seguinte com:

postgres  pg_dump -h localhost -p 5432 -U postgres stage_pesq > C:\stage_pesq.sql

e para acessar as tabelas usa o comando:

psql -h nomeservidor -U nomeusuario -d nomebancodedados < /caminho/nomearquivo.sql

↬→→→→→→→→→→→→→→→→→→→→→→→→→•••••←←←←←←←←←←←←←←←←←←←←←←←←←←←←↫

Tecnologias usadas:

<div style="display: inline_block"><br>
<img align="center"  height="100" width="100" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"/>
-
<img align="center"  height="150" width="150" src="https://i.imgur.com/Ko865kR.png" title="source: imgur.com"/>

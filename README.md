# README #

### Git ###

* Adionar aquivos *.pyc para serem ignorados pelo Git globalmente
```
#!cmd

git config --global core.excludesfile "c:\xampp\htdocs\simfaz\gitignore_pyc.txt"
```

### Instalação ###
 
* Criar um (virtualenv) na pasta /env do projeto
* Baixar as bibliotecas do Python utilizando o arquivo "/env/requirements.txt" com o pip
* Baixar as bibliotecas JavaScript utilizando o arquivo "/static/bower.json"
* Uma vez dentro do diretório simfaz/simfaz/static basta você executar `bower install`
* Caso você não tenho o bower, instale-o. `npm install bower`

### GDAL ###

* Para instalar no WINDOWS siga esse tutorial a risca: http://cartometric.com/blog/2011/10/17/install-gdal-on-windows/.
* De preferência instale gdal-111-1800-core.
* Para ter a biblioteca osgeo no seu python enviroment funcionando corretamente você vai ter que instalar.
* Quando instalar GDAL-1.11.3.win32-py2.7 você deve criar uma pasta temporária para extrair a lib essa lib GDAL-1.11.3.win32-py2.7 também para esse diretório.
* Quando você criar seu env no diretório do simfaz você deverá copiar e colar a o conteúdo dentro de site-packages para dentro do site-package the o virtualenv criou dentro de `env` (env é um diretório contendo a máquina virtual python para rodar o simfaz).

### Possíveis problemas ###

* Config' object has no attribute 'get_namespace
 Isso ocorre porque o método get_namespace está disponível somente a partir da versão 1.0 do Flask, por enquanto você deverá usar o seguinte comando para instalar esta versão:

```
#!cmd

pip install https://github.com/mitsuhiko/flask/tarball/master
```
Referência: [Pythonclub](http://pythonclub.com.br/what-the-flask-pt-2-flask-patterns-boas-praticas-na-estrutura-de-aplicacoes-flask)
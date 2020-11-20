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

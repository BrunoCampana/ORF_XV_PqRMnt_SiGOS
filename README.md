# Sistema de Gestão de Ordem de Serviço do Pq R Mnt12.

## Passos de Instalação:

* Instalar Python 3 e pip:
  sudo apt-get update && sudo apt-get -y upgrade
  sudo apt-get install python3
  sudo apt-get install -y python3-pip
  
* Instalar Django:
  sudo pip3 install django

* Instalar Django AdminLTE 2:
  pip3 install django-adminlte2
  
* Instalar MySQL
  ** Adicionar o MySQL ao repositório de Software
    cd /tmp
    curl -OL https://dev.mysql.com/get/mysql-apt-config_0.8.9-1_all.deb
    sudo dpkg -i mysql-apt-config*
    sudo apt-get update
    rm mysql-apt-config*
    
  ** Instalar MySQL Server package:
    sudo apt-get install mysql-server
    (Nota: durante a instalação, será configurada a senha para o 'root', que será utilizada no arquivo 'settings.py' do projeto. No projetom utilizamos a senha 'toor')
    
* Instalar MySQL Database Connector:
  sudo apt-get install python3-dev
  sudo apt-get install python3-dev libmysqlclient-dev
  sudo pip3 install mysqlclient
  sudo apt-get install mysql-server

* Criar o banco de dados:
  mysql -u root -p         (entrar com a senha root)
  >> create database sigos;
  
## Alguns comandos úteis do django:
  python3 manage.py makemigrations  -  Responsável por criar novas migrações de acordo com mudanças observadas nos modelos
  python3 manage.py migrate  -  Realiza as migrações de fato
  python3 manage.py runserver  - Roda a aplicação
  python3 manage.py createsuperuser - Cria um usuário com privilégios de administrador




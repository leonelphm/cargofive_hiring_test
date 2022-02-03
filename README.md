# CargoFive Hiring Test

# Para instalar la apliacacion en modo desarrollo debera seguir los siguientes pasos:


## 1-) Instalar el controlador de versiones git:
 
    $ su

    # aptitude install git

## 2-) Descargar el codigo fuente del proyecto Hiring Test:


    Para descargar el código fuente del proyecto contenido en su repositorio GIT realice un clon del proyecto, con el siguiente comando:

    $ git clone https://github.com/leonelphm/cargofive_hiring_test.git
                
## 3-) Instalar Dependencias:

    
    El proyecto está desarrollado con el lenguaje de programación Python, se debe instalar Python-3.8.5, si se encuentra en una distribucion de GNU/Linux puede seguir los paso que se encuentran en este enlace para hacer la instalacion de python 3.8.5 ![instala python](https://caotic.co/install-or-configure/instalar-python-3-8-en-ubuntu-debian/), si no logra instalar la version mas reciente con estos paso puede instalar ![Pyenv](https://realpython.com/intro-to-pyenv/) para el manejo de varias versiones de python en su sistema operativo.

    Se debe tener instalado virtualenv y virtualenvwrapper

    Al terminar de instalar todas las dependencias iniciales del sistema, se deber crear el entorno virtual de la siguiente manera:
    
    mkvirtualenv cargofive

## 4-) Instalar los requerimientos del proyecto:

Para activar el ambiente virtual cargofive ejecute el siguiente comando:

    workon cargofive

Con el comando anterio se activa el ambiente virtual quedando la consola asi **(cargofive)$**:

Ingresar al directorio raiz del proyecto:

    (cargofive)$ cd cargofive_hiring_test

    (cargofive)cargofive_hiring_test$ 

Desde ahi se deben instalar los requirimientos del proyecto con el siguiente comando:

    (cargofive)cargofive_hiring_test$  pip install -r requirements_dev.txt

De esta manera se instalaran todos los requerimientos para montar el proyecto.

## 5-) Crear base de datos y Migrar los modelos:

El manejador de base de datos que usa el proyecto, por ahora, es sqlite3


Si quieres iniciar una aplicacion desde 0 solo debes usar el comando:

    python manage.py makemigrations

y luego

    python manage.py migrate

El cual generara todas las tablas de la base de datos.



## 6-) Iniciar la aplicacion:

Para iniciar la apliacion se debe ejecutar el siguiente comando:

    (cargofive)cargofive_hiring_test$ python manage.py runserver

Ingresar a la plataforma en la ruta: localhost:8000


Puede iniciar sesion desde el admin con las siguientes credenciales:

username: admin
password: 123administrador

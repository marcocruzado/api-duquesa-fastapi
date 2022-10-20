# PROYECTO LA DUQUESA SALÓN & SPA

<b>Descripción del proyecto:</b>
<br>
Este es un proyecto para un Salón & Spa llamado La Duquesa donde tendremos lo siguiente:
<br>
- Todas las transacciones que se han realizado en el centro.
- Todos los servicios que se ofrecen en el centro.
- Todas los categorías de los servicios que se ofrecen en el centro.
- Todos los usuarios que se han registrado en el centro.
- Todos los roles que se han registrado en el centro.

<b>Requisitos:</b>
<br>
Para poder ejecutar el proyecto se necesita tener instalado:
<ol>
<li>virtualenv</li>
<li>python 3.8</li>
<li>fastapi</li>
<li>uvicorn</li>
<li>serverless</li>
<li>nodejs</li>
<li>npm</li>
<li>serverless-python-requirements</li>
</ol>

<b>Instalación:</b>
<br>
Para poder instalar el proyecto se debe seguir los siguientes pasos:
<ol>
<li>Clonar el proyecto.</li>
<li>Crear un entorno virtual.</li>
<li>Activar el entorno virtual.</li>
<li>Instalar las dependencias.</li>
</ol>

<b>Clonar el proyecto:</b>
<br>
```
git clone https://github.com/marcoantoniocruzado1994/api-duquesa-fastapi.git
```

<b>Crear un entorno virtual:</b>
<br>
```
virtualenv venv
```

<b>Activar el entorno virtual:</b>
<br>
```
source venv/bin/activate
```

<b>Instalar las dependencias:</b>
<br>
```
pip install -r requirements.txt
```

<b>Ejecutar npm install</b>
<br>
```
npm install
```

# <b>Local:</b>

## Primera forma:
<p> la instalacion con FastAPI</p>
<br>
Para poder ejecutar el proyecto en local se debe seguir los siguientes pasos:
<ol>
<li>Activar el entorno virtual.</li>
<li>Ejecutar el proyecto.</li>
</ol>

<b>Activar el entorno virtual:</b>
<br>
```
source venv/bin/activate
```

<b>Ejecutar el proyecto:</b>
<br>
```
uvicorn main:app --reload
```
<br>

## Segunda forma:
<p> Con Docker</p>
<br>
Para poder ejecutar el proyecto en local se debe seguir los siguientes pasos:

<b>Ejecutar el contenedor:</b>
<br>
```
docker build -t imagen-duqueza:0.1.2 .
``` 
luego de ejecutar el comando anterior se debe ejecutar el siguiente comando:
```
docker run --name duqueza-container -p 8000:8000 imagen-duqueza:0.1.2
```

## Previo al despliegue

Para poder desplegar el proyecto se debe tener en cuenta lo siguiente:

- Se debe tener una cuenta en AWS.
- Se debe tener instalado serverless.

luego de estos dos puntos tienes que configurar tu cuenta de AWS en serverless, para esto debes ejecutar el siguiente comando:

```
serverless config credentials --provider aws --key <key> --secret <secret>
```

Y si vas a usar Cloud9 para desplegar el proyecto debes ejecutar el siguiente comando:

```
serverless config credentials --provider aws --key <key> --secret <secret> --profile cloud9
```

Para que así al hacer el deploy se encuentre con tu cuenta de AWS.
<br><br>

<b>Despliegue:</b>
<br>

Para poder desplegar el proyecto se debe seguir los siguientes pasos:
<ol>
<li>Instalar serverless</li>
<li>Instalar serverless-python-requirements</li>
</ol>

<b>Instalar serverless:</b>
<br>
```
npm install -g serverless
```

<b>Instalar serverless-python-requirements:</b>
<br>
```
npm install --save-dev serverless-python-requirements
```
<br>

## Desplegar el proyecto

Para poder desplegar el proyecto se debe ejecutar el siguiente comando:
```
serverless deploy --stage dev
```
<br>

### Endpoints

El proyecto cuenta con los siguientes endpoints:

- GET /transaction/detail
- GET /transaction/detail/{transaction_id}
- POST /transaction/new

- GET /role/detail
- GET /role/detail/{role_id}
- POST /role/new

- GET /service/detail
- GET /service//detail/{service_id}
- GET /service/detail_by_category/{category_id}
- POST /service/new

- GET /additional/detail
- GET /additional/detail/{additional_id}
- GET /additional/detail_by_service/{service_id}
- POST /additional/new

- GET /category/detail
- GET /category/detail/{category_id}
- POST /category/new

- GET /user/detail
- GET /user/detail/{user_id}
- POST /user/new
- POST /user/login
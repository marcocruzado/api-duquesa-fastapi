# PROYECTO SPA-DUQUESA

<b>Descripción del proyecto:</b>
<br>
Este es un proyecto para un centro de estética, en el cual se puede consultar:
<br>

- Todas las trasnacciones que se han realizado en el centro.
- Todos los Servicios que se ofrecen en el centro.
- Todas los categorías de los servicios que se ofrecen en el centro.
- Todos los usuarios que se han registrado en el centro.
- Todos los roles que se han registrado en el centro.

<b>Requisitos:</b>
<br>
para poder ejecutar el proyecto se necesita tener instalado:
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
<li>Clonar el proyecto</li>
<li>Crear un entorno virtual</li>
<li>Activar el entorno virtual</li>
<li>Instalar las dependencias</li>
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

<b>Despliegue:</b>
<br>
Para poder desplegar el proyecto se debe seguir los siguientes pasos:
<ol>
<li>instalar serverless</li>
<li>instalar serverless-python-requirements</li>
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

## Previo al despliegue

Para poder desplegar el proyecto se debe tener en cuenta lo siguiente:

- Se debe tener una cuenta en AWS.
- Se debe tener instalado serverless.

luego de estos dos puntos tienes que configurar tu cuenta de AWS en serverless, para esto debes ejecutar el siguiente comando:

```
serverless config credentials --provider aws --key <key> --secret <secret>
```
y si vas a usar cloud9 para desplegar el proyecto debes ejecutar el siguiente comando:

```
serverless config credentials --provider aws --key <key> --secret <secret> --profile cloud9
```


para que asi al hacer el deploy este con tu cuenta de AWS.

## Desplegar el proyecto
<br>
Para poder desplegar el proyecto se debe ejecutar el siguiente comando:

```
serverless deploy --stage dev
```



### Endpoints
inicialmente el proyecto cuenta con los siguientes endpoints:

- GET /transactions
- GET /transactions/{id}
- POST /transactions
- GET /role
- GET /role/{id}
- POST /role






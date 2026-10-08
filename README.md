# Sesión 5 · IA/ML & Data Analytics en AWS

Material de la sesión sobre servicios de **IA/ML** y **Data Analytics** de AWS
(nivel AWS Cloud Practitioner), del AWS Student Builder Group · Universidad del Valle.

## Contenido

- **`Sesion 5 - IA y Analytics.pptx`** — la presentación de la sesión.
- **`demo-rekognition/`** — Lab en vivo 1: IA de **visión**. Subes una foto y
  Amazon Rekognition te dice qué ve en ella.
- **`demo-comprehend/`** — Lab en vivo 2: IA de **lenguaje**. Escribes un texto y
  Amazon Comprehend te da el sentimiento, el idioma y las entidades.

## Cómo hacer los labs

Cada carpeta de demo tiene su propio **`README.md`** con el paso a paso completo
(copiar y pegar, desde la consola de AWS). Ambos labs son serverless
(**API Gateway + Lambda**) y entran en la capa gratuita.

Orden recomendado: empieza por **Rekognition** (es más visual) y luego **Comprehend**.

> 💡 Al probar la página web, **no la abras con doble clic**. Sírvela por HTTP desde
> la carpeta del lab:
> ```bash
> python3 -m http.server 8000
> ```
> y abre `http://localhost:8000/probar-api.html`. Cada README explica por qué.

## Arquitectura de los labs

```
Navegador  →  API Gateway  →  AWS Lambda (Python)  →  Servicio de IA de AWS
```

El navegador (la página `probar-api.html`) llama a una API, la API dispara una
función Lambda, y la Lambda llama al servicio de IA (Rekognition o Comprehend) y
devuelve el resultado. No hay servidores que administrar.

---

## Glosario · palabras que te vas a encontrar

Si alguna palabra de los labs te suena a chino, búscala aquí. Están explicadas en
simple, con analogías.

### Conceptos de la nube

- **AWS (Amazon Web Services):** la nube de Amazon. En vez de comprar tus propios
  servidores, le "alquilas" a Amazon lo que necesites y pagas solo por lo que usas.
- **Región:** la zona del mundo donde viven tus recursos (ej. `us-east-1` = Norte de
  Virginia). ⚠️ Importante: crea TODO en la **misma región**, o las piezas no se ven
  entre sí. Es el error nº1.
- **Consola de AWS:** la página web donde administras AWS con clics (lo que usas en
  los labs).
- **Capa gratuita (free tier):** una cantidad de uso gratis al mes el primer año.
  Estos labs entran ahí: no te cobran.
- **Serverless (sin servidores):** no es que no haya servidores; es que **tú no los
  administras**. AWS los enciende y apaga solo cuando hace falta. Tú solo pones el
  código.

### Servicios que usamos

- **Lambda:** una función (un trozo de código) que AWS ejecuta solo cuando alguien la
  llama. No tienes un servidor prendido todo el día: corre, responde y se apaga.
  Aquí la escribimos en **Python**.
- **API Gateway:** la "puerta de entrada" a tu código. Crea una **URL pública** que,
  cuando alguien la llama, dispara tu Lambda. Es el puente entre la web e Internet y
  tu función.
- **IAM (Identity and Access Management):** el sistema de **permisos** de AWS. Decide
  quién puede hacer qué. Por defecto todo está prohibido: por eso hay que darle
  permiso explícito a la Lambda para que use Rekognition o Comprehend.
- **Rol (de ejecución):** la "identidad" que toma tu Lambda al correr. Los permisos
  (IAM) se le pegan a ese rol.
- **Política (policy):** el documento (en JSON) que lista qué acciones se permiten.
  Ej: "esta Lambda PUEDE llamar a `comprehend:DetectSentiment`".
- **Amazon Rekognition:** servicio de IA que **analiza imágenes y videos** (detecta
  objetos, escenas, caras, texto). Solo acepta imágenes **JPG o PNG**.
- **Amazon Comprehend:** servicio de IA de **lenguaje (NLP)**. Lee un texto y te da el
  **sentimiento** (positivo/negativo), el **idioma** y las **entidades** (nombres,
  lugares, fechas).
- **NLP (Procesamiento de Lenguaje Natural):** el campo de la IA que hace que las
  máquinas "entiendan" texto humano. Es lo que hace Comprehend.

### Términos técnicos de la web

- **API:** una forma de que dos programas se hablen. Tú llamas a una URL con una
  petición y te devuelve una respuesta (normalmente en **JSON**).
- **JSON:** un formato de texto para intercambiar datos, con llaves `{ }`. Es como van
  y vienen los datos entre la web, la API y la Lambda.
- **HTTP / HTTPS:** el "idioma" con el que el navegador habla con las webs y APIs.
  HTTPS es HTTP cifrado (seguro).
- **Endpoint / Invoke URL:** la **dirección** de tu API (ej.
  `https://xxxx.execute-api.us-east-1.amazonaws.com`). Es lo que pegas en la página
  web para que sepa a dónde llamar.
- **Ruta (route) y método:** la ruta es el camino dentro de la API (ej. `/analizar`) y
  el método es el tipo de petición. En los labs usamos **POST** (enviar datos).
- **POST / GET / OPTIONS:** tipos de petición HTTP. **GET** = pedir/leer, **POST** =
  enviar datos, **OPTIONS** = una pregunta previa que hace el navegador (ver *preflight*).
- **CORS (Cross-Origin Resource Sharing):** una regla de seguridad del **navegador**.
  Por defecto, una web NO puede llamar a una API de otro "origen" (otro dominio).
  Activar CORS en API Gateway es decirle: "sí, permito que esta web me llame". Si está
  mal, verás el error **"CORS error"**. 👉 Regla fácil de los labs: en CORS,
  **Methods = POST y OPTIONS**, **Headers = `content-type`**; no cruces las casillas.
- **Preflight:** la petición **OPTIONS** que el navegador manda ANTES del POST para
  "preguntar permiso". Si ves que el OPTIONS da **204 OK** pero el POST falla, el
  problema está en CORS o en la Lambda, no en el preflight.
- **Origen (origin):** el "de dónde viene" una petición (dominio + puerto). Si abres el
  HTML con **doble clic**, el origen es `null` (`file://`) y el navegador bloquea la
  llamada. Por eso lo servimos con `python3 -m http.server` → origen `http://localhost`.
- **localhost:** tu propia computadora vista como un servidor web. `http://localhost:8000`
  es "sírveme la página desde aquí mismo".
- **base64:** una forma de convertir una imagen (bytes) en **texto** para poder
  enviarla dentro de un JSON. Así viaja la foto del navegador a la Lambda en el lab de
  Rekognition.
- **Timeout:** el tiempo máximo que puede correr la Lambda antes de que AWS la corte.
  Por defecto son 3 segundos; en los labs lo subimos para que dé tiempo a responder.
- **CloudWatch (Logs):** donde AWS guarda los **registros** de tu Lambda. Si algo falla
  con error 500, ahí ves el mensaje real del porqué.

### Errores que verás (y qué significan)

- **"CORS error":** el navegador bloqueó la llamada. Casi siempre: abriste el HTML con
  doble clic (usa `localhost`) o cruzaste las casillas de CORS.
- **404 (Not Found):** la ruta no existe. Revisa que sea exactamente **POST `/analizar`**.
- **500 (Internal Server Error):** la Lambda corrió pero falló. Normalmente le falta un
  **permiso** (IAM) o se quedó sin **tiempo** (timeout). Mira **CloudWatch Logs**.
- **"InvalidImageFormatException":** (solo Rekognition) la imagen no es JPG ni PNG.
  Buena señal igual: significa que todo lo demás ya funciona.

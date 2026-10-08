# Mini proyecto: entiende textos con Amazon Comprehend

¡Bienvenido/a! Vas a construir una **IA de lenguaje** sin servidores. Al final tendrás
una página web donde escribes un **texto** (una opinión, un comentario, una reseña) y
la inteligencia artificial te dice:

- el **sentimiento** (positivo, negativo, neutral o mixto),
- el **idioma** detectado, y
- las **entidades clave** (personas, lugares, fechas, organizaciones...).

El camino de tus datos será:

**Navegador  →  API Gateway  →  Lambda (Python)  →  Amazon Comprehend**

- **Lo que necesitas:** tu laptop y tu cuenta de AWS.
- **Tiempo:** unos 20 minutos.
- **Costo:** entra en la capa gratuita (50.000 unidades/mes el primer año).

> Sigue los pasos en orden. Si algo falla, mira **"¿Algo salió mal?"** al final.

---

## Antes de empezar

1. Usa la **misma región** que indique el presentador (ej: `us-east-1` / N. Virginia).
   Créalo TODO en esa misma región (función y API).
2. Ten a mano los archivos de esta carpeta: `lambda_function.py`,
   `politica-comprehend.json` y `probar-api.html`.

---

## Paso 1 · Crea la función Lambda (4 min)

1. En la consola de AWS busca **Lambda** y entra.
2. Clic en **Create function** (Crear función).
3. Elige **Author from scratch** (Crear desde cero).
4. **Function name:** `apiComprehend`
5. **Runtime:** elige **Python 3.12** (o la versión de Python más nueva que aparezca).
6. Clic en **Create function**.
7. En la pestaña **Code** (Código), borra lo que hay y **pega todo** el contenido de
   `lambda_function.py`.
8. Clic en **Deploy** (Implementar) para guardar los cambios.

> 💡 Recomendado: en **Configuration → General configuration → Edit**, sube el
> **Timeout** a **15 segundos**. La función hace tres llamadas a Comprehend.

✅ Tu función ya tiene la lógica para mandar el texto a Comprehend.

---

## Paso 2 · Dale permiso a la Lambda para usar Comprehend (5 min)

> Este es el paso más importante. Por defecto, la Lambda **no puede** llamar a
> Comprehend. Hay que darle permiso.

1. En tu función, ve a **Configuration** (Configuración) → **Permissions** (Permisos).
2. En **Execution role** (Rol de ejecución), haz clic en el **nombre del rol**
   (se abre IAM en otra pestaña).
3. En IAM, clic en **Add permissions** (Agregar permisos) → **Create inline policy**
   (Crear política insertada).
4. Elige la pestaña **JSON** y pega el contenido de `politica-comprehend.json`.
5. Clic en **Next** → ponle un nombre como `AccesoComprehend` → **Create policy**.

✅ Ahora tu Lambda puede pedirle a Comprehend que analice textos.

---

## Paso 3 · Crea la API con API Gateway (5 min)

1. En la consola busca **API Gateway** y entra.
2. Clic en **Create API** y en **HTTP API** elige **Build**.
3. **Integrations:** clic en **Add integration** → elige **Lambda** → selecciona tu función `apiComprehend`.
4. **API name:** `ApiComprehend` → **Next**.
5. En **Configure routes** (Configurar rutas), crea esta ruta apuntando a tu Lambda:
   - **Method:** `POST`  · **Resource path:** `/analizar`
6. **Next** hasta **Create**.
7. Cuando se cree, copia la **Invoke URL** (algo como
   `https://xxxxxx.execute-api.us-east-1.amazonaws.com`).

✅ Ya tienes una API pública conectada a tu Lambda.

---

## Paso 4 · Activa CORS (2 min)

> CORS es lo que permite que tu página web (que corre en tu equipo) pueda llamar a la API.

1. En tu API, en el menú lateral entra a **CORS**.
2. Clic en **Configure** y rellena cada campo con MUCHO cuidado de no equivocarte de casilla:

   | Campo | Qué poner |
   |---|---|
   | **Access-Control-Allow-Origin** | `*` |
   | **Access-Control-Allow-Methods** | `POST` y `OPTIONS` |
   | **Access-Control-Allow-Headers** | `content-type` |
   | **Access-Control-Expose-Headers** | *(déjalo vacío)* |

3. Guarda los cambios.
4. Dale al botón **Deploy / Implementación** para que la etapa tome el cambio.

> ⚠️ **Error muy común:** cruzar las casillas. Los **métodos** (`POST`, `OPTIONS`)
> van SOLO en *Allow-Methods*, y `content-type` va SOLO en *Allow-Headers*.
> Si pones `post`/`options` en *Allow-Headers* o `content-type` en *Expose-Headers*,
> la llamada fallará con "CORS error".
> Truco para recordarlo: **Methods = verbos** (POST/OPTIONS), **Headers = content-type**.

---

## Paso 5 · ¡Pruébala desde el navegador! (4 min)

> ⚠️ **No abras el HTML con doble clic.** Si lo haces, corre como `file://` y el
> navegador lo trata como "origen null" y BLOQUEA la llamada (verás "CORS error"
> aunque CORS esté bien). Hay que servirlo por `http://localhost`.

1. Abre una terminal **dentro de esta carpeta** (`demo-comprehend`) y ejecuta:
   ```bash
   python3 -m http.server 8000
   ```
2. En el navegador abre: **http://localhost:8000/probar-api.html**
3. En el campo de arriba, **pega la Invoke URL** de tu API (la del Paso 3).
4. Escribe un texto, por ejemplo:
   *"Me encantó el servicio, el equipo de Bogotá fue muy amable."*
5. Pulsa **Analizar texto**.
6. Verás el **sentimiento** (Positivo), el **idioma** (es) y las **entidades**
   detectadas (Bogotá como lugar). 🎉

Prueba también con una queja o con un texto en inglés. Verás cómo cambian el
sentimiento y el idioma.

✅ Acabas de usar un servicio de **IA de lenguaje (NLP)** en una app real.

---

## ¿Qué aprendiste?

| Lo que hiciste | Concepto de AWS |
|---|---|
| Escribiste un texto y te dio el sentimiento | **Amazon Comprehend** (NLP) |
| Detectó el idioma y las entidades | **Comprehend** (detección de idioma y entidades) |
| Escribiste la función | **AWS Lambda** (código sin servidores) |
| Diste el permiso con la política | **IAM** (seguridad y accesos) |
| Creaste la API con ruta POST | **API Gateway** |
| Todo junto, sin servidores | **Arquitectura serverless** |

Lo potente: **no entrenaste ningún modelo de lenguaje**. Comprehend ya venía
entrenado por AWS. Tú solo hiciste la llamada.

---

## Limpieza (hazlo al terminar)

Para no dejar recursos activos:

1. **API Gateway** → selecciona `ApiComprehend` → **Delete**.
2. **Lambda** → selecciona `apiComprehend` → **Actions** → **Delete**.

> El rol de IAM se puede borrar también desde IAM si quieres dejar todo limpio.

---

## ¿Algo salió mal?

### Los 2 tropiezos más comunes (nos pasaron en vivo)

Estos dos son los que casi todos encuentran al conectar la web con la API.

**1. "No se pudo conectar / CORS error" pero abriste el HTML con doble clic**

- **Síntoma:** en la consola del navegador (F12 → Network) ves que el `OPTIONS`
  (preflight) responde **204 OK**, pero el `POST` (fetch) sale como **CORS error**.
  Arriba puede decir `(blocked:origin)`. En el Monitor de la Lambda **no aparece
  ninguna invocación**.
- **Por qué:** abriste `probar-api.html` con doble clic, así que corre como `file://`.
  El navegador le asigna "origen null" y bloquea el POST antes de que salga.
- **Solución:** sírvelo por HTTP. En la carpeta `demo-comprehend` corre
  `python3 -m http.server 8000` y abre `http://localhost:8000/probar-api.html`.

**2. "CORS error" aunque sirvas el HTML por localhost**

- **Síntoma:** el preflight da 204 pero el POST sigue en "CORS error".
- **Por qué:** se cruzaron las casillas de CORS. El caso típico: los métodos
  (`post`, `options`) quedaron en *Allow-Headers* y `content-type` en *Expose-Headers*,
  dejando *Allow-Methods* vacío ("No se permiten métodos").
- **Solución:** repite el **Paso 4** y revisa que cada valor esté en su casilla:
  **Methods = POST y OPTIONS**, **Headers = content-type**, **Expose-Headers vacío**.
  Guarda y dale **Deploy / Implementación**.

### Tabla rápida de errores

| Lo que ves | Qué pasó | Cómo arreglarlo |
|---|---|---|
| "No se pudo conectar" al abrir con doble clic | El HTML corre como `file://` (origen null) y el navegador bloquea el POST | Sírvelo por http: `python3 -m http.server 8000` y abre `http://localhost:8000/probar-api.html` (ver tropiezo 1) |
| "CORS error" con el POST (preflight da 204) | Se cruzaron las casillas de CORS | Revisa el Paso 4: Methods = POST/OPTIONS, Headers = content-type (ver tropiezo 2) |
| En el Monitor de la Lambda no hay invocaciones | El POST ni siquiera llega a la Lambda | Casi siempre es el `file://` del tropiezo 1 |
| Error 500 al analizar | La Lambda no tiene permiso de Comprehend | Repite el Paso 2 (la política IAM) |
| "Task timed out" en los logs | Las llamadas tardaron más de lo permitido | Sube el **Timeout** de la Lambda a 15 s (Paso 1, nota) |
| La ruta da 404 | El path no es `/analizar` | Revisa el Paso 3: ruta POST en `/analizar` |
| "El texto no puede estar vacío" | Pulsaste analizar sin escribir | Escribe un texto primero |
| El idioma sale raro | El texto es muy corto | Comprehend acierta mejor con una frase completa |

> 💡 **Cómo depurar como un pro:** abre **F12 → Network** y mira el POST a `/analizar`.
> Si no hay invocaciones en la Lambda → es el navegador (origen/CORS). Si hay
> invocaciones pero da 500 → es la Lambda (mira **CloudWatch logs** desde
> Lambda → Monitor → View CloudWatch logs).

---

## Archivos de esta carpeta

- **`README.md`** → esta guía.
- **`lambda_function.py`** → el código que pegas en la Lambda (Paso 1).
- **`politica-comprehend.json`** → el permiso IAM (Paso 2).
- **`probar-api.html`** → la página para probar tu API (Paso 5).

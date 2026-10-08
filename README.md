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

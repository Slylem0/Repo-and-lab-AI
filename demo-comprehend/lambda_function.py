import json
import boto3

# Cliente de Amazon Comprehend (procesamiento de lenguaje natural)
comprehend = boto3.client("comprehend")

# Comprehend necesita saber el idioma para el sentimiento y las entidades.
# Idiomas que soporta el analisis de sentimiento (los mas comunes).
IDIOMAS_SOPORTADOS = {"es", "en", "fr", "de", "it", "pt", "ar", "hi", "ja", "ko", "zh"}

# Nombres amigables para mostrar el sentimiento en espaniol
SENTIMIENTO_ES = {
    "POSITIVE": "Positivo",
    "NEGATIVE": "Negativo",
    "NEUTRAL": "Neutral",
    "MIXED": "Mixto",
}


def responder(codigo, cuerpo):
    """Arma la respuesta HTTP con las cabeceras CORS para que el navegador la acepte."""
    return {
        "statusCode": codigo,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS",
        },
        "body": json.dumps(cuerpo, ensure_ascii=False),
    }


def lambda_handler(event, context):
    metodo = event.get("requestContext", {}).get("http", {}).get("method", "POST")

    # El navegador manda una peticion OPTIONS antes del POST (CORS). La respondemos OK.
    if metodo == "OPTIONS":
        return responder(200, {"ok": True})

    try:
        datos = json.loads(event.get("body") or "{}")
    except Exception:
        return responder(400, {"error": "JSON invalido"})

    texto = (datos.get("texto") or "").strip()
    if not texto:
        return responder(400, {"error": "El texto no puede estar vacio"})

    try:
        # 1) Detectar el idioma dominante del texto
        det = comprehend.detect_dominant_language(Text=texto)
        idiomas = det.get("Languages", [])
        idioma = idiomas[0]["LanguageCode"] if idiomas else "en"
        idioma_conf = round(idiomas[0]["Score"] * 100, 1) if idiomas else 0

        # Comprehend solo analiza sentimiento/entidades en idiomas soportados.
        # Si viene algo raro, caemos a ingles para no fallar.
        idioma_analisis = idioma if idioma in IDIOMAS_SOPORTADOS else "en"

        # 2) Analizar el sentimiento (positivo, negativo, neutral, mixto)
        sent = comprehend.detect_sentiment(Text=texto, LanguageCode=idioma_analisis)
        sentimiento = SENTIMIENTO_ES.get(sent["Sentiment"], sent["Sentiment"])
        puntajes = {
            "Positivo": round(sent["SentimentScore"]["Positive"] * 100, 1),
            "Negativo": round(sent["SentimentScore"]["Negative"] * 100, 1),
            "Neutral": round(sent["SentimentScore"]["Neutral"] * 100, 1),
            "Mixto": round(sent["SentimentScore"]["Mixed"] * 100, 1),
        }

        # 3) Detectar entidades clave (personas, lugares, fechas, organizaciones...)
        ent = comprehend.detect_entities(Text=texto, LanguageCode=idioma_analisis)
        entidades = [
            {"texto": e["Text"], "tipo": e["Type"], "confianza": round(e["Score"] * 100, 1)}
            for e in ent.get("Entities", [])
        ]
    except Exception as e:
        return responder(500, {"error": "Comprehend fallo: " + str(e)})

    return responder(200, {
        "idioma": idioma,
        "idioma_confianza": idioma_conf,
        "sentimiento": sentimiento,
        "puntajes": puntajes,
        "entidades": entidades,
    })

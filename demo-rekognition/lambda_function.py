import json
import base64
import boto3

# Cliente de Amazon Rekognition (vision por computadora)
rekognition = boto3.client("rekognition")


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

    # Leemos el cuerpo que envia la pagina web (una imagen en base64)
    try:
        datos = json.loads(event.get("body") or "{}")
    except Exception:
        return responder(400, {"error": "JSON invalido"})

    imagen_b64 = datos.get("imagen")
    if not imagen_b64:
        return responder(400, {"error": "No llego ninguna imagen"})

    # La pagina manda algo como "data:image/jpeg;base64,XXXX". Nos quedamos con el XXXX.
    if "," in imagen_b64:
        imagen_b64 = imagen_b64.split(",", 1)[1]

    try:
        bytes_imagen = base64.b64decode(imagen_b64)
    except Exception:
        return responder(400, {"error": "La imagen no se pudo decodificar"})

    # Llamada a Rekognition: detecta etiquetas (objetos, escenas, conceptos)
    try:
        resultado = rekognition.detect_labels(
            Image={"Bytes": bytes_imagen},
            MaxLabels=10,
            MinConfidence=70,
        )
    except Exception as e:
        return responder(500, {"error": "Rekognition fallo: " + str(e)})

    # Dejamos solo lo que nos interesa: nombre + confianza (%)
    etiquetas = [
        {"nombre": e["Name"], "confianza": round(e["Confidence"], 1)}
        for e in resultado.get("Labels", [])
    ]

    return responder(200, {"total": len(etiquetas), "etiquetas": etiquetas})

import requests
import time

# === CONFIGURACIÓN ===

# Token de Twitter (API v2)
TWITTER_BEARER = 'AAAAAAAAAAAAAAAAAAAAAEPY0gEAAAAAQPYkUWaAqgcsqrNkeajtc5x48k4%3DKsJwAqx01kbqG2J95vhXtoohgqjjz8iLBOzQidTdFVPbQMb3ys'  # Reemplaza con tu Bearer Token

# Configuración de Telegram
TELEGRAM_TOKEN = '7543006002:AAF3qUj53r7SQl_713Lvwu8076OM8fhmvt8'  # Reemplaza con tu Bot Token
TELEGRAM_CHAT_ID = '901297365'  # Reemplaza con tu Chat ID

# Palabras clave de memecoins
query = '(#DOGE OR #PEPE OR #SHIB OR #SOLANA OR #TRUMPCOIN OR #memecoin) -is:retweet lang:en'

# Twitter API URL
twitter_url = 'https://api.twitter.com/2/tweets/search/recent'
headers = {
    'Authorization': f'Bearer {TWITTER_BEARER}',
}

params = {
    'query': query,
    'max_results': 10,  # Cambié el valor de 5 a 10 (maximo permitido por Twitter)
    'tweet.fields': 'created_at,text,author_id',
}


def get_tweets():
    """Obtiene tweets recientes de Twitter con manejo de errores"""
    response = requests.get(twitter_url, headers=headers, params=params)
    if response.status_code == 429:  # Si hay demasiadas solicitudes
        print("Demasiadas solicitudes. Esperando 15 minutos...")
        time.sleep(15 * 60)  # Espera de 15 minutos
        return get_tweets()  # Intenta nuevamente después de la espera
    elif response.status_code != 200:
        print('Error al conectar con Twitter:', response.status_code, response.text)
        return []
    data = response.json()
    return data.get('data', [])


def send_telegram_message(text):
    """Envía el mensaje a Telegram"""
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    res = requests.post(url, data=payload)
    if res.status_code != 200:
        print("❌ Error al enviar mensaje a Telegram:", res.text)


# === LOOP PRINCIPAL ===

print("🚀 Empezando a rastrear tweets sobre memecoins...")

enviados = set()  # para evitar repetir los mismos tweets

while True:
    tweets = get_tweets()

    for tweet in tweets:
        tweet_id = tweet['id']
        if tweet_id not in enviados:
            text = f"🧵 Nuevo tweet sobre memecoin:\n\n{tweet['text']}\n\n🕒 {tweet['created_at']}"
            send_telegram_message(text)
            enviados.add(tweet_id)

    time.sleep(240)  # Espera 2 minutos antes de volver a revisar

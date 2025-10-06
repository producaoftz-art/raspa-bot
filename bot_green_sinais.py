import os
import asyncio
import random
from datetime import datetime, timedelta
import pytz
from telegram import Bot
from telegram.constants import ChatAction

# 🔐 CONFIGURAÇÕES
# Lendo o TOKEN e CHAT_ID das variáveis de ambiente
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Erro: As variáveis de ambiente TOKEN e CHAT_ID não foram configuradas.")
    print("Por favor, adicione-as nas configurações do Render.")
    exit()

bot = Bot(token=TOKEN)

# 🎰 Sites, raspadinhas e prêmios com probabilidades
SITES = {
    "https://goldvip777.site": {
        "IPhone 17 Pro Max": {"prob": 20, "premios": {"Airpods Pro": 40, "Apple Watch Ultra 3": 30, "Macbook M3 Apple": 30}},
        "Sempre Ganhe": {"prob": 50, "premios": {"1000 reais": 25, "200 reais": 50, "5000 reais": 25}},
        "Vivara Premiada": {"prob": 30, "premios": {"Pulseira Vivara Ouro 18k": 40, "500 reais": 60}}
    },
    "https://clickvip777.com/": {
        "Apple Premiada": {"prob": 30, "premios": {"Iphone 16 Pro Max": 10, "Apple Watch Ultra": 10, "500 reais": 30, "100 reais": 30, "Iphone 14 Pro": 20}},
        "Moto dos Sonhos": {"prob": 20, "premios": {"Moto Honda Biz": 10, "200 reais": 50, "1000 reais": 20, "3000 reais": 20}},
        "Sempre Ganhe": {"prob": 50, "premios": {"5 mil reais": 15, "3 mil reais": 15, "1 mil reais": 30, "200 reais": 40}}
    }
}

# Lista de nomes (para feedback)
NOMES = [
    "Luanne", "Thierry", "Aislan", "Yanca", "Breno S.", "Calebe", "Maikon",
    "Evellyn", "Kauan R.", "Dayse", "Jardel", "Brunna", "Allan T.", "Laercio",
    "Camylle", "Deivison", "Murillo", "Rafaelly", "Thales", "Yasmin L.",
    "Giovana M.", "Henrick", "Monique", "Davi M.", "Kaio", "Letícia A.",
    "Fabrício", "Nayara", "Vinícius C.", "Heitor G.", "Edmundo", "Raissa",
    "Taylon", "Nicolas R.", "Hellen", "Thayná", "Emanuel", "Valentina", "Diogo",
    "Leandra", "Caue", "Enzo P.", "Isadora", "Roberta", "Marlon", "Tatiane",
    "Douglas A.", "Ingrid", "Luciano", "Alanys", "Gustavo F."
]

def escolher_com_peso(opcoes):
    nomes = list(opcoes.keys())
    pesos = [opcoes[n]["prob"] if isinstance(opcoes[n], dict) else opcoes[n] for n in nomes]
    return random.choices(nomes, weights=pesos, k=1)[0]

TITULOS = [
    "🟢💚 *VAI SAIR UM {premio_upper}!* 💥",
    "🚨 *SINAL QUENTE!* Vai sair um {premio_upper} 🔥",
    "🎰 *Novo Sinal:* {premio_upper}! 💸",
]

FRASES_FINAIS = [
    "⚡💰 *Jogue rapidamente dentro desse tempo e garanta seu prêmio!* 🏆",
    "🎯💎 *Aposte agora e não perca esse prêmio incrível!* 💰",
    "🚀🎰 *Entre nesse tempo e conquiste o seu prêmio!* 💎",
    "💚🏆 *Garanta o seu agora, o tempo é curto!* ⚡",
    "🔥💸 *Jogue rápido e aproveite a sorte!* 🎰"
]

async def enviar_sinal():
    fuso = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(fuso)

    site = random.choice(list(SITES.keys()))
    raspadinha = escolher_com_peso(SITES[site])
    premio = escolher_com_peso(SITES[site][raspadinha]["premios"])

    minutos_aleatorios = random.randint(1, 5)
    horario_base = agora + timedelta(minutes=minutos_aleatorios)
    segundos = sorted(random.sample(range(5, 55), 3))
    horarios_segundos = [f"{horario_base.strftime('%Hh:%Mm')}{s:02d}s" for s in segundos]
    horarios_formatados = " | ".join(horarios_segundos)

    chance = random.randint(80, 100)
    titulo = random.choice(TITULOS).format(premio_upper=premio.upper())
    frase_final = random.choice(FRASES_FINAIS)

    mensagem = (
        f"{titulo}\n\n"
        f"🎯 *Raspadinha:* `{raspadinha}`\n"
        f"🕒 *Horário:* `{horarios_formatados}`\n"
        f"🔗 *Acessar site:* [Clique aqui]({site})\n\n"
        f"💹 *Chance de acerto:* `{chance}%`\n\n"
        f"{frase_final}"
    )

    msg = await bot.send_message(chat_id=CHAT_ID, text=mensagem, parse_mode="Markdown")

    ultimo_segundo = segundos[-1]
    tempo_final = horario_base.replace(second=ultimo_segundo)
    espera = (tempo_final - datetime.now(fuso)).total_seconds()
    await asyncio.sleep(max(0, espera))

    # Simula "digitando..." antes do feedback
    tempo_digitando = random.randint(2, 5)
    await bot.send_chat_action(chat_id=CHAT_ID, action=ChatAction.TYPING)
    await asyncio.sleep(tempo_digitando)

    # Gera resultado após o tempo final
    resultado = random.choices(["GREEN", "RED"], weights=[70, 30])[0]

    # Define tipo de grupo (FREE/PREMIUM) com probabilidades
    grupo_tipo = random.choices(["FREE", "PREMIUM"], weights=[30, 70])[0]

    # Escolhe um nome aleatório da lista
    nome = random.choice(NOMES)

    # Apaga a mensagem do sinal
    await bot.delete_message(chat_id=CHAT_ID, message_id=msg.message_id)

    # Monta o texto de feedback
    if resultado == "GREEN":
        texto = f"🟢🟢🟢 *GREEN!* 🟢🟢🟢\n\nParabéns ao ganhador que está no grupo {grupo_tipo}: *{nome}* 🎉💸"
        if grupo_tipo == "PREMIUM":
            texto += (
                "\n\n💰 Acesse nosso grupo premium e tenha *sinais de alta qualidade*, "
                "feito por nossos especialistas! 📈💬\n"
                "Suporte 24h para receber os prêmios e maior chance de ganhos! 💎"
            )
    else:
        texto = "🔴🔴🔴 *RED!* 🔴🔴🔴\n\nInfelizmente o sinal não veio 😞 Vamos tentar novamente! 💪"

    # Envia o feedback
    await bot.send_message(chat_id=CHAT_ID, text=texto, parse_mode="Markdown")

async def main():
    print("🤖 Bot Green Sinais iniciado e enviando automaticamente...")
    while True:
        await enviar_sinal()
        intervalo = random.randint(20, 300)
        print(f"⏱️ Próximo sinal em {intervalo}s...")
        await asyncio.sleep(intervalo)

if __name__ == "__main__":
    asyncio.run(main())
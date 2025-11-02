# psk_vip_bot.py
from telethon import TelegramClient, events
import asyncio
import random, re

# === KONFIGURACJA ===
api_id = 24410825
api_hash = "1af7fdb76b96212d2189a1cd14ebfd1f"
source_channel = "https://t.me/+Vkcfjcl669ZjZjFi"   # wklej swój source (link prywatny lub @nazwa lub ID)
target_channel = "https://t.me/+zMnt781-wrkyNDNk"   # wklej swój target (link prywatny lub @nazwa lub ID)
session_name = "psk_user_session 2"  # nazwa pliku sesji - zmień, jeśli chcesz oddzielne konto
# ====================


def modify_numbers(text: str, direction: str) -> str:
    """
    Modyfikuje liczby w tekście (Entry i Targets):
    LONG -> obniża o 0.2–0.5%
    SHORT -> podnosi o 0.2–0.5%
    """
    def adjust(match):
        try:
            number = float(match.group())
        except:
            return match.group()
        if direction == "long":
            change = random.uniform(-0.005, -0.002)  # -0.5% do -0.2%
        elif direction == "short":
            change = random.uniform(0.002, 0.005)   # +0.2% do +0.5%
        else:
            change = 0
        new_number = number * (1 + change)
        # zachowaj 2 miejsca po przecinku (dostosuj jeśli potrzeba)
        return f"{new_number:.2f}"

    # dopasuj liczby z kropką (np. 123.45) — typowe dla cen
    return re.sub(r"\b\d+\.\d+\b", adjust, text)


def modify_text(text: str) -> str:
    # Usuń linki i niepotrzebne znaki
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[*_`]", "", text)

    # Usuń godzinę (np. 20:33)
    text = re.sub(r"\b\d{1,2}:\d{2}\b", "", text)

    # Sprawdź kierunek (long / short)
    direction = None
    if re.search(r"\bLONG\b", text, re.IGNORECASE):
        direction = "long"
    elif re.search(r"\bSHORT\b", text, re.IGNORECASE):
        direction = "short"

    # Delikatnie modyfikuj wartości tylko dla long/short
    text = modify_numbers(text, direction)

    # Ustal nagłówek (można dynamicznie dodać emoji w zależności od kierunku)
    header = "💎 PSK VIP Club:\n📊 Market Update:\n"
    if direction == "long":
        header = "💎 PSK VIP Club:\n🟢 LONG Signal:\n"
    elif direction == "short":
        header = "💎 PSK VIP Club:\n🔴 SHORT Alert:\n"

    # Stopka
    footer = "\n📌 Exclusive for VIP members\n👉 @CryptoBossVIP"

    return f"{header}\n{text.strip()}\n{footer}"


import os

async def main():
    session_path = os.path.join(os.path.dirname(__file__), "user_session.session")
    client = TelegramClient(session_path.replace(".session", ""), api_id, api_hash)

    await client.start()  # tu pojawi się prośba o numer przy pierwszym uruchomieniu
    me = await client.get_me()
    print(f"✅ Logged in as: {me.username or me.first_name} ({me.id})")
    print("✅ User-bot started, listening only for TEXT messages...")

   

    


    @client.on(events.NewMessage(chats=source_channel))
    async def handler(event):
        try:
            msg = event.message

            # Pomijaj media
            if msg.media:
                return

            # Pomijaj puste wiadomości
            if not msg.text:
                return

            # Losowe opóźnienie (60–120 sekund)
            delay = random.randint(60, 120)
            await asyncio.sleep(delay)

            # Modyfikacja i wysyłka
            modified_text = modify_text(msg.text)
            await client.send_message(target_channel, modified_text, parse_mode="html")

        except Exception as e:
            print(f"❌ Error: {e}")

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())





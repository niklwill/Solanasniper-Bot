# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 07:43:39 2025

@author: niklwill
""

import os
import base58
import requests
import json
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.account import Account
from dotenv import load_dotenv

# Lade Umgebungsvariablen
load_dotenv()

# Solana Konfiguration
RPC_URL = os.getenv("PRIVATE_RPC")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Verbinde zur Solana Blockchain
solana_client = Client(RPC_URL)

# Wandle den Private Key um
try:
    private_key_bytes = base58.b58decode(PRIVATE_KEY)
    account = Account(private_key_bytes)
    print(f"✅ Erfolgreich mit Wallet verbunden: {account.public_key()}")
except Exception as e:
    print(f"❌ Fehler bei Private Key Konvertierung: {e}")
    exit()

# API-Endpunkte für DEX-Daten
API_ENDPOINTS = {
    "raydium": "https://api.raydium.io/v2/sdk/liquidity",
    "orca": "https://api.orca.so/pools",
    "serum": "https://api.serum-vial.dev/v1/pools",
}

# Liquiditätspools abrufen
def get_liquidity_pools():
    pools = []
    for dex, url in API_ENDPOINTS.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                pools.extend(data)
                print(f"✅ {dex} Pools geladen: {len(data)}")
            else:
                print(f"⚠️ Fehler beim Abruf von {dex}: {response.status_code}")
        except Exception as e:
            print(f"❌ Fehler bei {dex}: {e}")
    return pools

# Einfacher Trade (Testfunktion)
def place_trade():
    transaction = Transaction()
    print("🚀 Trade ausgeführt (Testmodus)")

# Hauptfunktion
if __name__ == "__main__":
    pools = get_liquidity_pools()
    if pools:
        print(f"🎯 {len(pools)} Pools gefunden. Start Sniping...")
        place_trade()
    else:
        print("❌ Keine Pools gefunden. Beende...")


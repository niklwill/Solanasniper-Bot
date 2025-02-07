import { Connection, Keypair, PublicKey, Transaction, sendAndConfirmTransaction } from "@solana/web3.js"
import dotenv from "dotenv";
dotenv.config();

console.log("Private Key:", process.env.PRIVATE_KEY);
console.log("RPC Endpoint:", process.env.PRIVATE_RPC);

import fetch from "node-fetch";
import bs58 from "bs58";
import dotenv from "dotenv";
dotenv.config();

// Deine Helius RPC URL (ersetze durch deinen eigenen API Key)
const PRIVATE_RPC = "https://mainnet.helius-rpc.com/?api-key=03364cae-c434-41ae-b25a-70efc490d68d";  
const connection = new Connection(PRIVATE_RPC, {
    commitment: "confirmed",
    wsEndpoint: "wss://mainnet.helius-rpc.com"
});

// Dein Solflare Private Key (Base58)
const secretKey = bs58.decode("5USf5kR7z2w9ZHKcmpE4vBmHJwDNRGvHLwCctBsBrk1UthMdbfM4P6cu3n7A7L8cGndYqR4kn1phMLEnjLh1b8WD");
const wallet = Keypair.fromSecretKey(secretKey);

const DEX_APIS = {
    raydium: "https://api.raydium.io/v2/sdk/liquidity",
    orca: "https://api.orca.so/pools",
    serum: "https://api.serum-vial.dev/v1/pools"
};

// Vertrauenswürdige Pools (IDs müssen noch angepasst werden)
const TRUSTED_POOLS = ["POOL_ID_1", "POOL_ID_2", "POOL_ID_3"];
const MIN_LIQUIDITY = 10000;
const MAX_PRICE = 0.1;

async function getDynamicSlippage(price) {
    const volatilityFactor = 0.001; // Anpassung je nach Marktbedingungen
    return price * (1 + volatilityFactor);
}

async function getPools(DEX) {
    try {
        const response = await fetch(DEX_APIS[DEX]);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Fehler beim Abrufen der ${DEX} Pools:`, error);
    }
}

async function findSnipingOpportunity() {
    for (const dex in DEX_APIS) {
        const pools = await getPools(dex);
        for (const pool of pools) {
            if (TRUSTED_POOLS.includes(pool.id) && pool.liquidity > MIN_LIQUIDITY && pool.price < MAX_PRICE) { 
                console.log(`Sniping-Möglichkeit auf ${dex}: ${pool.id} zu Preis ${pool.price}`);
                await executeTrade(pool.id, pool.price, dex);
            }
        }
    }
}

async function executeTrade(poolId, price, dex) {
    try {
        const adjustedPrice = await getDynamicSlippage(price);
        console.log(`Trade auf ${dex} Pool: ${poolId} zum Preis: ${adjustedPrice}`);

        // Hier sollte die Logik für den Trade eingebaut werden (z. B. Raydium Swap)

        console.log("Trade abgeschlossen!");
    } catch (error) {
        console.error("Trade fehlgeschlagen:", error);
    }
}

async function startSniping() {
    console.log("Sniper-Bot wird gestartet...");
    setInterval(findSnipingOpportunity, 3000);
}

startSniping();


const bs58 = require('bs58');
const fs = require('fs');

// Dein Array-Key
const keyArray = [204,99,23,72,93,21,192,191,197,19,50,166,220,39,178,90,140,85,29,164,171,18,26,31,82,82,176,123,170,225,162,150,88,120,133,12,5,73,81,141,229,54,212,124,6,206,206,16,106,95,126,97,5,85,158,193,53,15,7,204,197,137,51,105];

// In Buffer umwandeln
const keyBuffer = Buffer.from(keyArray);

// In Base58 umwandeln
const base58Key = bs58.encode(keyBuffer);

// In Datei speichern
fs.writeFileSync('private_key_base58.txt', base58Key);

console.log('Base58 Private Key gespeichert in private_key_base58.txt');

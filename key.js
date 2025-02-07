const bs58 = require('bs58');
const fs = require('fs');

// Dein Array-Key
const keyArray = [212,54,3,170,3,64,201,158,20,108,170,140,144,198,235,16,119,200,152,22,34,181,167,249,91,42,104,149,22,99,41,176,58,39,211,6,186,49,217,9,81,75,155,165,12,210,156,169,188,9,16,232,25,194,192,217,155,161,44,131,193,72,70,236];

// In Buffer umwandeln
const keyBuffer = Buffer.from(keyArray);

// In Base58 umwandeln
const base58Key = bs58.encode(keyBuffer);

// In Datei speichern
fs.writeFileSync('private_key_base58.txt', base58Key);

console.log('Base58 Private Key gespeichert in private_key_base58.txt');
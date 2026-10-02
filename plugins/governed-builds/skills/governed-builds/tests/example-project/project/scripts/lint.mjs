import { readFileSync } from 'node:fs';
if (readFileSync('src/slugify.mjs', 'utf8').includes('var ')) process.exit(1);
console.log('lint passed');

import assert from 'node:assert/strict';
import { slugify } from '../src/slugify.mjs';
assert.equal(slugify('Hello World'), 'hello-world');
console.log('tests passed');

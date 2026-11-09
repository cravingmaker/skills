import test from 'node:test';
import assert from 'node:assert/strict';
import {query} from 'fixture-boundary';
test('public query',async()=>assert.deepEqual((await query('select 1')).rows,[]));

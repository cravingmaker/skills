import assert from 'node:assert/strict';
import test from 'node:test';
import {sum} from '../src/index.ts';
test('adds', () => assert.equal(sum(2, 3), 5));

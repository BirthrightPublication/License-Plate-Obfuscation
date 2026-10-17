import {test} from 'node:test';
import assert from 'node:assert/strict';
import {states,validate,legalRecord,availability,parseProject,statuses,risks} from '../src/domain.js';
test('all 50 states are selectable without duplicates',()=>{assert.equal(states.length,50);assert.equal(new Set(states).size,50);});
test('invalid preview text is rejected; valid preview never implies jurisdictional approval',()=>{for(const text of ['', '<SCRIPT>', 'ABCDEFGHIJKLM'])assert.equal(validate('California',text).status,'invalid');assert.equal(validate('California','STUDIO').status,'unverified');assert.equal(validate('Unknown','A').status,'invalid');});
test('legal classifications and risk are independent; no evidence means no risk score',()=>{assert.deepEqual(statuses,['Legal','Illegal','Obscure','Unverified']);assert.equal(risks.length,5);for(const state of states){const r=legalRecord(state);assert.equal(r.classification,'Unverified');assert.equal(r.risk,null);assert.equal(r.verifiedAt,null);}});
test('availability fails closed',()=>assert.equal(availability().status,'unavailable'));
test('project roundtrip and defensive import',()=>{const p={schemaVersion:1,name:'Study',state:'Texas',text:'ABC123'};assert.deepEqual(parseProject(JSON.parse(JSON.stringify(p))),p);for(const value of [null,{}, {...p,schemaVersion:2},{...p,state:'Other'},{...p,name:'a'.repeat(81)}])assert.throws(()=>parseProject(value));assert.equal(parseProject({...p,extra:'ignored'}).extra,undefined);});

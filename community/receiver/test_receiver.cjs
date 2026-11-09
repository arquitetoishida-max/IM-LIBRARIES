const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(__dirname + '/Code.gs', 'utf8');

function receiver(responses, configured = true) {
  const rows = [['request_id', 'state', 'issue_number', 'issue_url', 'received_at', 'payload_json', 'last_error']];
  const calls = [];
  const sheet = {
    getLastRow: () => rows.length,
    appendRow: row => rows.push([...row]),
    getDataRange: () => ({getValues: () => rows.map(row => [...row])}),
    getRange: (row, column, count = 1, width = 1) => ({
      getValues: () => rows.slice(row - 1, row - 1 + count).map(value => value.slice(column - 1, column - 1 + width)),
      setValues: values => { rows[row - 1] = [...values[0]]; },
      createTextFinder: target => ({matchEntireCell: () => ({findNext: () => {
        const index = rows.findIndex((value, index) => index >= row - 1 && value[column - 1] === target);
        return index < 0 ? null : {getRow: () => index + 1};
      }})})
    })
  };
  const context = {
    PropertiesService: {getScriptProperties: () => ({getProperty: key => configured ? {GITHUB_TOKEN: 'test-token', QUEUE_SPREADSHEET_ID: 'test-sheet'}[key] : null})},
    SpreadsheetApp: {openById: () => ({getSheetByName: () => sheet}), flush: () => {}},
    ContentService: {MimeType: {JSON: 'application/json'}, createTextOutput: output => ({output, setMimeType() {return this;}})},
    LockService: {getScriptLock: () => ({tryLock: () => true, releaseLock: () => {}})},
    UrlFetchApp: {fetch: (url, options) => {
      calls.push({url, options});
      const next = responses.shift();
      if (next instanceof Error) throw next;
      if (!next) throw new Error('unexpected request');
      return {getResponseCode: () => next.code, getContentText: () => JSON.stringify(next.body)};
    }}
  };
  vm.createContext(context);
  vm.runInContext(source, context);
  const post = value => JSON.parse(context.doPost({postData: {contents: JSON.stringify(value)}}).output);
  return {context, rows, calls, post};
}

const report = {
  schema_version: 1, request_id: '2b222afe-e063-47ac-b163-a1e18574c870',
  language: 'ja', entry_id: 'ja:en:000000179', english_id: 'en:000000179',
  package_id: 'ja-core-v2', package_version: '2.2.0', app_version: '0.9.149',
  message: '場所 e 地方 — há um erro nesta palavra. ``` @someone'
};
const created = {code: 201, body: {number: 123, html_url: 'https://github.com/arquitetoishida-max/IM-LIBRARIES/issues/123'}};

{
  const service = receiver([]);
  const fields = JSON.parse(JSON.stringify(vm.runInContext('REPORT_FIELDS', service.context)));
  const schema = JSON.parse(fs.readFileSync(__dirname + '/../report.schema.json', 'utf8'));
  assert.deepEqual([...fields].sort(), Object.keys(schema.properties).sort());
  assert.equal(schema.properties.message.maxLength, 10000);
}

{
  const service = receiver([created]);
  const result = service.post(report);
  assert.equal(result.status, 'received');
  assert.equal(result.issue_number, 123);
  assert.equal(service.post(Object.fromEntries(Object.entries(report).reverse())).issue_number, 123);
  assert.equal(service.post({...report, english_sense_id: null, form_id: null}).issue_number, 123);
  assert.equal(service.calls.length, 1);
  assert.equal(service.post({...report, message: 'Different message'}).code, 'request_id_conflict');
  const body = JSON.parse(service.calls[0].options.payload).body;
  assert.ok(body.includes('````\n' + report.message + '\n````'));
  assert.ok(!body.includes('test-token'));
  assert.equal(JSON.parse(service.rows[1][5]).message, report.message);
}
{
  const service = receiver([]);
  for (const value of [{...report, message: ' '}, {...report, request_id: 'bad'}, {...report, account_id: 'private'}, {...report, word: null}, {...report, created_at: '11/09/2026'}, {...report, message: 'x'.repeat(10001)}]) {
    assert.equal(service.post(value).status, 'rejected');
  }
  assert.equal(service.calls.length, 0);
}
{
  const service = receiver([new Error('response lost')]);
  assert.equal(service.post(report).status, 'pending');
  assert.equal(service.post(report).status, 'pending');
  assert.equal(service.calls.length, 1);
  const body = JSON.parse(service.calls[0].options.payload).body;
  service.context.UrlFetchApp.fetch = () => ({getResponseCode: () => 200, getContentText: () => JSON.stringify({items: [{number: 999, html_url: created.body.html_url, body: 'Request ID: ' + report.request_id}]})});
  service.context.reconcilePendingReports();
  assert.equal(service.post(report).status, 'pending');
  service.context.UrlFetchApp.fetch = () => ({getResponseCode: () => 200, getContentText: () => JSON.stringify({items: [{number: 123, html_url: created.body.html_url, body}]})});
  service.context.reconcilePendingReports();
  assert.equal(service.post(report).issue_number, 123);
}
{
  const service = receiver([{code: 403, body: {}}, created]);
  assert.equal(service.post(report).status, 'retry');
  assert.equal(service.post(report).status, 'received');
  assert.equal(service.calls.length, 2);
}
{
  const service = receiver([], false);
  assert.equal(service.post(report).status, 'retry');
  assert.equal(service.calls.length, 0);
  assert.equal(service.rows.length, 1);
}
{
  const service = receiver([]);
  service.context.LockService.getScriptLock = () => ({tryLock: () => false});
  assert.equal(service.post(report).status, 'retry');
  assert.equal(service.rows.length, 1);
}
console.log('PASS receiver service mocks: receipt, idempotency, conflict, validation, uncertain reconciliation, definite failure, configuration and busy lock');

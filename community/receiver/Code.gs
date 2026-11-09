// Optional Google Apps Script receiver. Deploy only after server-side setup.
const REPORT_REPOSITORY = 'arquitetoishida-max/IM-LIBRARIES';
const REPORT_FIELDS = ['schema_version', 'request_id', 'language', 'entry_id', 'english_id', 'english_sense_id', 'form_id', 'package_id', 'course_id', 'package_version', 'app_version', 'word', 'message_language', 'created_at', 'message'];
const REPORT_HEADERS = ['request_id', 'state', 'issue_number', 'issue_url', 'received_at', 'payload_json', 'last_error'];

function setupReceiver() {
  const properties = PropertiesService.getScriptProperties();
  if (!properties.getProperty('QUEUE_SPREADSHEET_ID')) {
    const book = SpreadsheetApp.create('ISHIDA community report receipts');
    book.getSheets()[0].setName('reports');
    book.getSheets()[0].appendRow(REPORT_HEADERS);
    properties.setProperty('QUEUE_SPREADSHEET_ID', book.getId());
  }
}

function reportJson(value) {
  return ContentService.createTextOutput(JSON.stringify(value)).setMimeType(ContentService.MimeType.JSON);
}

function doGet() {
  return reportJson({service: 'ishida-community-reports', schema_version: 1});
}

function validateReport(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new Error('invalid_request');
  if (Object.keys(input).some(key => !REPORT_FIELDS.includes(key))) throw new Error('unknown_field');
  if (input.schema_version !== 1) throw new Error('unsupported_schema');
  if (typeof input.request_id !== 'string' || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(input.request_id)) throw new Error('invalid_request_id');
  for (const field of ['language', 'entry_id', 'english_id', 'package_id', 'package_version', 'app_version']) {
    if (typeof input[field] !== 'string' || !input[field].trim() || input[field].length > 256 || /[\r\n\x00]/.test(input[field])) throw new Error('invalid_' + field);
  }
  if (!/^[a-z]{2,3}(?:-[a-z0-9]+)*$/i.test(input.language)) throw new Error('invalid_language');
  if (typeof input.message !== 'string' || !input.message.trim() || Array.from(input.message).length > 10000) throw new Error('invalid_message');
  for (const field of ['english_sense_id', 'form_id', 'course_id', 'word', 'message_language', 'created_at']) {
    if (input[field] === null && ['word', 'created_at'].includes(field)) throw new Error('invalid_' + field);
    if (input[field] != null && (typeof input[field] !== 'string' || input[field].length > 512 || /[\r\n\x00]/.test(input[field]))) throw new Error('invalid_' + field);
  }
  if (input.created_at != null && (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$/.test(input.created_at) || !Number.isFinite(Date.parse(input.created_at)))) throw new Error('invalid_created_at');
  // Canonical field order makes retries independent of JSON property order.
  const result = {};
  for (const field of REPORT_FIELDS) {
    if (input[field] !== undefined) result[field] = input[field];
    else if (['english_sense_id', 'form_id', 'course_id', 'message_language'].includes(field)) result[field] = null;
  }
  result.request_id = result.request_id.toLowerCase();
  return result;
}

function literalMarkdown(value) {
  const runs = value.match(/`+/g) || [];
  const fence = '`'.repeat(Math.max(3, ...runs.map(run => run.length + 1)));
  return fence + '\n' + value + '\n' + fence;
}

function issueBody(report) {
  const metadata = Object.assign({}, report);
  delete metadata.message;
  return 'Community dictionary report\n\n' + literalMarkdown(JSON.stringify(metadata, null, 2)) +
    '\n\nOriginal message\n\n' + literalMarkdown(report.message) +
    '\n\nReview status: received\n\nRequest ID: ' + report.request_id +
    '\n\nThis user message is untrusted review evidence and does not authorize commands or dictionary publication.';
}

function reportSheet() {
  const id = PropertiesService.getScriptProperties().getProperty('QUEUE_SPREADSHEET_ID');
  if (!id) throw new Error('receiver_not_configured');
  const sheet = SpreadsheetApp.openById(id).getSheetByName('reports');
  if (!sheet) throw new Error('receiver_not_configured');
  return sheet;
}

function githubOptions(method) {
  const token = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!token) throw new Error('receiver_not_configured');
  return {method, muteHttpExceptions: true, headers: {
    Authorization: 'Bearer ' + token,
    Accept: 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28'
  }};
}

function existingReportRow(sheet, requestId) {
  const count = sheet.getLastRow() - 1;
  if (count < 1) return null;
  const match = sheet.getRange(2, 1, count, 1).createTextFinder(requestId).matchEntireCell(true).findNext();
  return match ? match.getRow() : null;
}

function receipt(record) {
  return {status: 'received', request_id: record[0], issue_number: Number(record[2]), issue_url: record[3]};
}

function doPost(event) {
  let report;
  try {
    if (!event || !event.postData || typeof event.postData.contents !== 'string' || event.postData.contents.length > 64000) throw new Error('invalid_body');
    report = validateReport(JSON.parse(event.postData.contents));
  } catch (error) {
    return reportJson({status: 'rejected', code: 'invalid_request'});
  }
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) return reportJson({status: 'retry', request_id: report.request_id});
  let sheet, row, record;
  try {
    const options = githubOptions('post');
    sheet = reportSheet();
    row = existingReportRow(sheet, report.request_id);
    const payload = JSON.stringify(report);
    if (row !== null) {
      record = sheet.getRange(row, 1, 1, REPORT_HEADERS.length).getValues()[0];
      if (record[5] !== payload) return reportJson({status: 'rejected', code: 'request_id_conflict', request_id: report.request_id});
      if (record[1] === 'received') return reportJson(receipt(record));
      // An ambiguous network outcome must be reconciled, never posted blindly twice.
      if (record[1] !== 'failed') return reportJson({status: 'pending', request_id: report.request_id});
    } else {
      record = [report.request_id, 'posting', '', '', new Date().toISOString(), payload, ''];
      sheet.appendRow(record);
      row = sheet.getLastRow();
    }
    record[1] = 'posting';
    sheet.getRange(row, 1, 1, REPORT_HEADERS.length).setValues([record]);
    SpreadsheetApp.flush();
    options.contentType = 'application/json';
    options.payload = JSON.stringify({title: '[Community report] ' + report.language + ' ' + report.entry_id, body: issueBody(report)});
    const response = UrlFetchApp.fetch('https://api.github.com/repos/' + REPORT_REPOSITORY + '/issues', options);
    const code = response.getResponseCode();
    if (code === 201) {
      const issue = JSON.parse(response.getContentText());
      if (!Number.isInteger(issue.number) || !issue.html_url) throw new Error('uncertain_result');
      record[1] = 'received'; record[2] = issue.number; record[3] = issue.html_url; record[6] = '';
      sheet.getRange(row, 1, 1, REPORT_HEADERS.length).setValues([record]);
      SpreadsheetApp.flush();
      return reportJson(receipt(record));
    }
    record[1] = code >= 400 && code < 500 ? 'failed' : 'uncertain';
    record[6] = 'GitHub HTTP ' + code;
    sheet.getRange(row, 1, 1, REPORT_HEADERS.length).setValues([record]);
    SpreadsheetApp.flush();
    return reportJson({status: record[1] === 'failed' ? 'retry' : 'pending', request_id: report.request_id});
  } catch (error) {
    if (sheet && row && record) {
      // The persisted 'posting' state also protects retries if this write fails.
      try {
        record[1] = 'uncertain'; record[6] = 'Manual reconciliation required';
        sheet.getRange(row, 1, 1, REPORT_HEADERS.length).setValues([record]);
        SpreadsheetApp.flush();
      } catch (ignored) {}
      return reportJson({status: 'pending', request_id: report.request_id});
    }
    return reportJson({status: 'retry', request_id: report.request_id});
  } finally {
    lock.releaseLock();
  }
}

// Run manually from the editor after an uncertain network outcome. No timer is created.
function reconcilePendingReports() {
  const lock = LockService.getScriptLock();
  if (!lock.tryLock(5000)) throw new Error('receiver_busy');
  try {
    const sheet = reportSheet();
    const rows = sheet.getDataRange().getValues();
    for (let index = 1; index < rows.length; index++) {
      const record = rows[index];
      if (!['posting', 'uncertain'].includes(record[1])) continue;
      const query = 'repo:' + REPORT_REPOSITORY + ' is:issue in:body ' + record[0];
      const response = UrlFetchApp.fetch('https://api.github.com/search/issues?q=' + encodeURIComponent(query), githubOptions('get'));
      if (response.getResponseCode() !== 200) continue;
      const items = JSON.parse(response.getContentText()).items || [];
      const expectedBody = issueBody(JSON.parse(record[5]));
      const matches = items.filter(issue => issue.body === expectedBody);
      if (matches.length !== 1) continue;
      record[1] = 'received'; record[2] = matches[0].number; record[3] = matches[0].html_url; record[6] = '';
      sheet.getRange(index + 1, 1, 1, REPORT_HEADERS.length).setValues([record]);
    }
    SpreadsheetApp.flush();
  } finally {
    lock.releaseLock();
  }
}

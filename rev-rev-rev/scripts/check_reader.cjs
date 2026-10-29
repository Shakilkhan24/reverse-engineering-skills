// Optional Node.js check of the actual embedded reader script.
// This supplies a tiny DOM stub: it checks arithmetic and script execution,
// not browser layout, accessibility, printing or CSS rendering.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '..');
const page = fs.readFileSync(path.join(root, 'book.html'), 'utf8');
const script = page.match(/<script>([\s\S]*?)<\/script>/)[1];
const nodes = new Map();
function node(id) {
  if (!nodes.has(id)) nodes.set(id, {value: id === '#slow-count' ? '5' : '',
    textContent: '', style: {setProperty() {}}, handlers: {},
    addEventListener(name, handler) {this.handlers[name] = handler;},
    setAttribute() {}});
  return nodes.get(id);
}
const context = {Intl, document: {
  body: {style: {setProperty() {}}, classList: {toggle() {return true;}}},
  querySelector: node, querySelectorAll() {return [];},
  getElementById(id) {return node('#' + id);}
}, window: {addEventListener() {}, print() {}}};
vm.createContext(context);
vm.runInContext(script, context);
const nf = new Intl.NumberFormat('bn-BD', {maximumFractionDigits: 1});
const cases = [
  {slow: 0, mean: 105, p50: 100, p95: 100, p99: 200},
  {slow: 1, mean: 119, p50: 100, p95: 200, p99: 200},
  {slow: 5, mean: 175, p50: 100, p95: 200, p99: 1500},
  {slow: 6, mean: 189, p50: 100, p95: 1500, p99: 1500},
  {slow: 20, mean: 385, p50: 100, p95: 1500, p99: 1500}
];
for (const test of cases) {
  node('#slow-count').value = String(test.slow);
  node('#slow-count').handlers.input();
  for (const key of ['mean', 'p50', 'p95', 'p99']) {
    assert.equal(node('#' + key).textContent, nf.format(test[key]) + ' ms');
  }
}
const report = {executed_at_utc: new Date().toISOString(),
  book_sha256: crypto.createHash('sha256').update(page).digest('hex'),
  cases: cases.map(test => ({...test, result: 'PASS'})),
  scope: 'Actual embedded JavaScript with a DOM stub; numeric checks only, no browser rendering.'};
fs.mkdirSync(path.join(root, 'reports'), {recursive: true});
fs.writeFileSync(path.join(root, 'reports', 'reader-check.json'), JSON.stringify(report, null, 2) + '\n');
console.log('Reader arithmetic: 5 cases passed; no browser rendering test.');

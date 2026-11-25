// No browser or network required: verify when the external tracker may load.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../site_src/analytics.js'), 'utf8');
const endpoint = 'https://example.goatcounter.com/count';

function visit({url = 'https://wadelamble.github.io/constrained-improvisation/symmetry/',
                skip = false, configured = true, storageBlocked = false} = {}) {
  const values = new Map(skip ? [['skipgc', 't']] : []);
  const scripts = [], alerts = [], handlers = {};
  const context = {
    location: new URL(url),
    alert: message => alerts.push(message),
    localStorage: {
      getItem: key => { if (storageBlocked) throw Error('blocked'); return values.get(key); },
      setItem: (key, value) => { if (storageBlocked) throw Error('blocked'); values.set(key, value); },
    },
    document: {
      currentScript: {dataset: {endpoint: configured ? endpoint : ''}},
      createElement: () => ({dataset: {}}),
      head: {appendChild: script => scripts.push(script)},
    },
    window: {addEventListener: (name, handler) => { handlers[name] = handler; }},
  };
  vm.runInNewContext(source, context);
  return {scripts, alerts, values, handlers, context};
}

const normal = visit();
assert.equal(normal.scripts.length, 1);
assert.equal(normal.scripts[0].src, 'https://gc.zgo.at/count.js');
assert.equal(normal.scripts[0].dataset.goatcounter, endpoint);
assert.equal(visit({skip: true}).scripts.length, 0);
assert.equal(visit({configured: false}).scripts.length, 0);
assert.equal(visit({storageBlocked: true}).scripts.length, 0);
for (const url of [
  'http://localhost:8000/constrained-improvisation/',
  'https://wadelamble.github.io/another-project/',
  'https://wadelamble.github.io/constrained-improvisation/animation-review/',
  'https://wadelamble.github.io/constrained-improvisation/symmetry/contact-sheets/',
]) assert.equal(visit({url}).scripts.length, 0, url);
const optedOut = visit({url: 'https://wadelamble.github.io/constrained-improvisation/#exclude-my-visits'});
assert.equal(optedOut.scripts.length, 0);
assert.equal(optedOut.values.get('skipgc'), 't');
optedOut.handlers.hashchange();
assert.equal(optedOut.values.get('skipgc'), 't', 'Repeated use must not enable tracking');
normal.context.location.hash = '#exclude-my-visits';
normal.handlers.hashchange();
assert.equal(normal.values.get('skipgc'), 't', 'Same-page link must persist the exclusion');
console.log('Analytics checks passed: production loading, exclusion persistence, no local/review counting.');

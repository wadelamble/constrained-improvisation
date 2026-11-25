(() => {
  'use strict';

  const endpoint = document.currentScript?.dataset.endpoint || '';
  const base = '/constrained-improvisation';
  if (location.hostname !== 'wadelamble.github.io' ||
      !(location.pathname === base || location.pathname.startsWith(base + '/'))) return;

  // Use GoatCounter's own exclusion flag, so its tracker also honors this choice.
  function excludeOwnVisits() {
    if (location.hash !== '#exclude-my-visits') return false;
    try {
      localStorage.setItem('skipgc', 't');
      alert('Your visits from this browser will not be counted. Open this link in each browser you use.');
    } catch (_) {
      alert('This visit will not be counted, but this browser is blocking the storage needed to remember your choice.');
    }
    return true;
  }
  window.addEventListener('hashchange', excludeOwnVisits);
  if (excludeOwnVisits()) return;
  try {
    if (localStorage.getItem('skipgc') === 't') return;
  } catch (_) {
    return;
  }

  // Count the contents page and chapters, not review editions or media.
  const parts = location.pathname.slice(base.length).split('/').filter(Boolean);
  if (parts.length > 1 || parts[0] === 'animation-review') return;
  if (!/^https:\/\/[a-z0-9-]+\.goatcounter\.com\/count$/.test(endpoint)) return;

  const tracker = document.createElement('script');
  tracker.async = true;
  tracker.src = 'https://gc.zgo.at/count.js';
  tracker.dataset.goatcounter = endpoint;
  document.head.appendChild(tracker);
})();

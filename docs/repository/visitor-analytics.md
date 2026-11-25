# Visitor analytics

The production contents page and chapter pages use GoatCounter. Its endpoint is
configured by `ANALYTICS_ENDPOINT` in `scripts/build_site.py`; the small loader is
`site_src/analytics.js`. The dashboard is `https://constrainedimprovisation.goatcounter.com/`.

To exclude a browser, open:

https://wadelamble.github.io/constrained-improvisation/#exclude-my-visits

This saves GoatCounter's `skipgc` exclusion flag before loading its tracker.
Reopening the link keeps exclusion enabled. Do this separately in each browser
used on the laptop and phone. Clearing that browser's site data removes the
exclusion; private browsing uses separate storage. Local previews and the review
and contact-sheet editions are excluded automatically.

GoatCounter counts unique visits within its session window rather than treating
each reload as a new reader. It uses IP address plus browser information for up
to eight hours without retaining the raw addresses in its database. This is an
approximation of readers, not a permanent count of distinct people.

Run the focused loader checks with `node scripts/check_site_analytics.cjs`.
The checks do not send analytics requests. After changing the site, build and
run the usual `scripts/check_animation_review.py` delivery check as well.

References: [excluding own visits](https://www.goatcounter.com/help/skip-dev),
[sessions and visitors](https://www.goatcounter.com/help/sessions).

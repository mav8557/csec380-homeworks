# XSS Locations

There are at least two XSS locations in Armbook, both reflected and stored XSS vulnerabilities. HTML taken in the search bar is sanitized and reflected back in the search results, making it trivial to run arbitrary javascript in the browser.

Stored XSS occurs on the profile. Inputs are not sanitized and posts cannot be deleted, so any HTML put into them will be rendered in the page, including scripts.
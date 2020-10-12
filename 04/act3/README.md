# Clickjacking Jon Doe

To trick Jon Doe despite CSRF protections, we can still have success by performing clickjacking instead. Instead of sending a link or a page set to perform a request, we instead send a page with a hidden page on top of it, and a button that he would click. When he does his mouse actually clicks the hidden page's button on top, which adds us as a friend.


# Preventing the issue
There are a few ways to prevent clickjacking. One method is to use the X-Frame-Options header, which was designed just to solve this problem by telling a browser whether or not a page is allowed to be rendered in an iframe like in the example page.

A more modern approach is to use the CSP headers (Content Security Policy) which allow greater control over which pages are allowed to be rendered like in the demonstration.

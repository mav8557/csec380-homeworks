# Explanation

So in coming up with the CSP I had some trouble complying with the restrictions around unsafe operations and the script-src directive. Even though it is very possible to allow for the javascript to run via this directive, CSP by default flags calls to eval() and similar functions. jQuery, which Armbook is dependent on, actually calls eval() a few times in its code, including in a global context. So by default, CSP will actually prevent some key features of Armbook from running.

Whitelisting in CSP is not especially intended, or at least isn't with its own keyword or clear method of defining multiple of the same directive, to apply for different sources. To get around having to use unsafe-eval, I tried repeat directives and the following:

* Getting allowing by hash (redundant, since we've already allowed the javascript, just not eval())
* Usage of nonce (led to more errors and did not solve the problem, since it still blocked eval())
* Attempting to delay CSP (CSP applies as long as the browser is on the page, both before and after a page load)

Unfortunately, after several hours and many different strategies and configurations of each, I did not find a solution to this problem, as eval() was still blocked by my CSP. I did considerable research into this problem, especially considering jQuery, but did not find anything conclusive outside of passing unsafe-eval. As I had spent awhile on this requirement, and wanted to finish the assignment, I ended up setting unsafe-eval and continuing to make sure I finished everything on time. That being said, I'd be interested if possible in seeing how someone would go about solving this problem. Everything from the MDN documentation seemed to suggest that it could not be done within these conditions, and I would imagine that this is a common problem due to jQuery's continued popularity.  

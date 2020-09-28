# Writeup

## Is there certain information about the webserver that you can discern based on what files you can access?

Yes. I can assume that the server is being configured to support multiple different things, since there is both business/ and articles/ on the server. Aside from that the files we can access specifically does not tell a ton more about the technical qualities of the web server.

## Are there any ways to improve the speed of your scanner?

Using asynchronous I/O would improve things greatly. One method I considered was using coroutines instead of threads, which would be advantageous as the threads would not require locks to access critical regions, and would not depend on hindrances of the OS's scheduler. A language like Go would make these easier to implement, as well as the work queue. Using a coroutine would cut down on blocks and allow for much more consistent behavior as a result of that and not having to worry about locks.

I have made choices to use operators and data structures with efficient time complexity, including sets and associative arrays, but some string operations are repetitive. This would save time on a per request basis, but that difference would be much more noticeable without relying on locks as decided by Python's multiprocessing module.

## How can response codes be used in order to more efficiently search your site?

Response codes can be very efficient as they can tell a lot without having to rely on parsing the entire request for information. Response codes can tell us whether or not a page exists or simply is not viewable without authentication, for instance. If we received an unauthorized error we could conclude that the path does exist, and perhaps that other subpaths of that might be viewable by us, which is better than a 404. We could make a logical decision to route all requests through HTTPS if we get a 301 redirect on a plaintext request. This would be faster because then it doesn't have to constantly be redirected if the links on the site go to HTTP instead. We would redirect once instead of many times. Most obviously a 200 means that the path is correct, which can prompt further investigation down that path, a measure slightly different than just looking at page links. We could decide to go further down based on the status code and not just what happens to be linked on the page.

## Are there any common naming patterns that you might expect would yield positive results?

Yes. robots.txt shows anything that should not be indexed by search engines, which could contain links to sensitive or relevant information. /admin, /auth, /backup{,s}, and /.git could leak sensitive information. /.well-known could show metadata and other information about the server that could give other indicators to search as well.
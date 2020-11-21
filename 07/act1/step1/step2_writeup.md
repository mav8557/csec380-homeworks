# Writeup

Armbook now uses a session token ARM_SESSION to track user logins. It is actually created before the user logs in to the site, at index.php:

```php
<input type="password" id="password" name="password" />
<input type="hidden" id="session_id" name="ARM_SESSION" value="<?php if(!isset($_REQUEST["ARM_SESSION"])){echo substr(md5(time()),0,22);}else{echo htmlentities($_REQUEST["ARM_SESSION"]);} ?>" />
```

If the request variable is not set in the request to index.php it uses the current time, as opposed to a securely random value. Worse, if it is set it just uses that as the session token when the user logs in. 

If we craft a URL for index.php that specifies ARM_SESSION, a user that logs in from there will use the session id we choose. So that's what I do and send to the Hooli link clicker:

**https://csec380-core.csec.rit.edu:97/index.php?ARM_SESSION=notsecure**

If someone logs in using that link, it will create a session in the database and we can then request their homepage using the same session:

**https://csec380-core.csec.rit.edu:97/home.php?ARM_SESSION=notsecure**

This will show us Jon Doe's page, as seen in the two screenshots.

# Activity 2 Writeup

## Description

This exercise is a standard example of a GET based Cross-Site Request Forgery attack. We are tricking Jon into friending us by getting his browser to make a request on his behalf to add us.

To do that, we can look at the code for add_friend and see a id parameter in the GET request. In the code the SQL query is filled in with this query, and it is ultiamtely the user we want to add as a friend. So in order to get Jon to add us, we have to send him a link with our own user id passed as the parameter.

Finding this is a little tedious, I didn't think of a better way other than guessing. On the homepage if we view another user's page the same id parameter is there. I guessed a bit until I saw my own page, and then created this URL to put into the message board:

http://csec380-core.csec.rit.edu:84/add_friend.php?id=46

After the Hooli employee clicks it, the stored session is used to prove Jon's identity to Armbook and add ourselves.

## Fixing the vulnerability

To fix CSRF vulnerabilities, the only true solution is to use a CSRF token. Doing so correctly requires that the developer first ensure that parameters are not being passed by GET requests, which makes CSRF quite easy. Moving the parameters to POST doesn't fix the vulnerability, but it does make it less easy to perform. I didn't want to change armbook too much, so I chose not to go this route, but if it were my application then that is how I would go about it. To solidify the solution the server should generate a CSRF token when a user visits a page, included in the form that is submitted to the server. I used another parameter which is stored in the session

To resolve the issue, I create a CSRF token that gets added to a user's session on login, and then append it as another parameter to add and del_friend. In both of those scripts I check that the passed parameter is equal to what the server set. If not, then that request was likely made from outside of the site and should be ignored with a call to die().


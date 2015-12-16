<?php header('Content-type: xhtml'); echo '<?xml version="1.0" encoding="UTF-8"?>' ?>

<html xmlns="http://www.w3.org/1999/xhtml" 
      xmlns:svg="http://www.w3.org/2000/svg">
<head>
<title>Sealgair.com Weather</title>
<link rel="stylesheet" href="/sealgair.css" type="text/css" media="screen"/>
</head>
<body>
<div id="main">
<h1>Weather</h1>
<?php

$temppoints="";
$speedpoints="";

$db = sqlite3_open("/data/db/weather.db");
$now = time();
$start = time() - (60 * 60 * 24);
$interval = 60 * 5; 
$query = "select date, temp, speed, dir from weather where date > " . $start;
$result = sqlite3_query($db, $query);

$tempplot = 0;
$temptotal = 0;
$speedplot = 0;
$speedtotal = 0;
$n = 0;
$x = 42;
$t = $start + $interval;
while ($row = sqlite3_fetch_array($result)) {
	while ($row['date'] > $t) {
		if ($n > 0) {
			$tempplot = round($temptotal * 10 / $n);
			$temptotal = 0;
			$temppoints .= $x . "," . (300 - $tempplot) . " ";

			$speedplot = round($speedtotal * 10 / $n);
			$speedtotal = 0;
			$speedpoints .= $x . "," . (300 - $speedplot) . " ";

			$n = 0;
		}
		$t += $interval;
		$x += 2;
	} 

	$temp = $row['temp'];
	$speed = $row['speed'];
	$dir = $row['dir'];

	$temptotal += $temp;
	$speedtotal += $speed;
	$n++;
}

sqlite3_query_close($result);
sqlite3_close($db);

?>
<p>The latest weather at Carlston Cottage is:</p>
<ul>
<li><?php echo $temp ?> celsius</li>
<li><?php echo $speed ?> mph <?php echo $dir ?></li>
</ul>
<p>
This is the weather for the last 24 hours from 
<?php echo date("D M j G:i:s Y", $start); ?> to 
<?php echo date("D M j G:i:s Y T", $now); ?>.
</p>
<ul>
<li>Temperature is shown in <font color='blue'>blue</font></li>
<li>Wind speed is shown in <font color='green'>green</font>.</li>
</ul>
<p/>
<svg:svg xmlns:svg="http://www.w3.org/2000/svg"
   version="1.0" width="620" height="450">
  <svg:rect
          width="576" height="450" x="40" y="0" fill="none" stroke="blue" stroke-width="0.5"
	       id="rect6" />
  <svg:path d="M 35,400 L 40,400" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,350 L 40,350" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,300 L 40,300" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,250 L 40,250" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,200 L 40,200" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,150 L 40,150" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,100 L 40,100" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 35,50 L 40,50" fill="none" stroke="blue" stroke-width="0.5" />
  <svg:path d="M 64,298 L 64,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 88,298 L 88,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 112,298 L 112,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 136,298 L 136,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 160,298 L 160,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 184,298 L 184,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 208,298 L 208,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 232,298 L 232,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 256,298 L 256,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 280,298 L 280,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 304,298 L 304,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 328,298 L 328,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 352,298 L 352,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 376,298 L 376,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 400,298 L 400,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 424,298 L 424,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 448,298 L 448,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 472,298 L 472,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 496,298 L 496,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 520,298 L 520,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 544,298 L 544,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 568,298 L 568,302" stroke="gray" stroke-width="0.5" />
  <svg:path d="M 592,298 L 592,302" stroke="gray" stroke-width="0.5" />
  <svg:polyline points="40,100 616,100" stroke="gray" stroke-width="0.5" />
  <svg:polyline points="40,200 616,200" stroke="gray" stroke-width="0.5" />
  <svg:polyline points="40,300 615,300" stroke="gray" stroke-width="0.5" />
  <svg:polyline points="40,400 616,400" stroke="gray" stroke-width="0.5" />
  <svg:text x="27" y="304" font-size="12px">
       	<svg:tspan x="27" y="304">0</svg:tspan></svg:text>
  <svg:text x="20" y="204" font-size="12px">
  	<svg:tspan x="20" y="204">10</svg:tspan></svg:text>
  <svg:text x="20" y="104" font-size="12px">
  	<svg:tspan x="20" y="104">20</svg:tspan></svg:text>
  <svg:text x="15" y="404" font-size="12px">
  	<svg:tspan x="15" y="404">-10</svg:tspan></svg:text>
  <svg:text x="-275" y="20" transform="matrix(0,-1,1,0,0,0)" font-size="16px">
	<svg:tspan x="-275" y="20">Celsius</svg:tspan></svg:text>
  <svg:polyline points="<?php echo $temppoints; ?>" fill="none" stroke="blue" stroke-width="1" />
  <svg:polyline points="<?php echo $speedpoints; ?>" fill="none" stroke="green" stroke-width="0.5" />
</svg:svg>
</div>
</body>
</html>

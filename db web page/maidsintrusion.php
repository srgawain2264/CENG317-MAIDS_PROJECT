<!DOCTYPE html>
<html>
	<head>
		<title>MAIDS Intrusion LOG</title>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
		
		<style>



		th, td {
		border: 1px solid black;
		padding: 3px;
		}
		table {
		border: 1px dashed black;
		padding: 3px;
		margin-bottom:20px;
		border-spacing: 5px;
		}
		.center {
		display: block;
		margin-left: auto;
		margin-right: auto;
		width: 50%;
		}
		#footer {
		position: fixed;
		left: 0;
		bottom: 0;
		width: 100%;
		background-color: red;
		color: white;
		text-align: center;
		}
		p {
		text-align: center;
		}
		</style>
	</head>
		<body>
				


		<table style='width:100%'>
			<tr>
				<td><div class="header">
				<img src="/www/MAIDS_LOGO.png" style="width:300px;height:200px;" class="center"></a>
			</td>
			<td>
				<div style="text-align:center;padding:1em 0;"> <h3><a style="text-decoration:none;" href="https://www.zeitverschiebung.net/en/timezone/america--toronto"><span style="color:gray;">Current local time in</span><br />America/Toronto</a></h3> <iframe src="https://www.zeitverschiebung.net/clock-widget-iframe-v2?language=en&size=medium&timezone=America%2FToronto" width="100%" height="115" frameborder="0" seamless></iframe> </div>
			</td>
		</tr>
	</table>
</div>


<?php
$username = "root";
$password = "";
$database = "maids1";
$mysqli = new mysqli("localhost", $username, $password, $database);
$query = "SELECT * FROM maidsintrusion";
echo "<br> <br>";
if ($result = $mysqli->query($query)) {
while ($row = $result->fetch_assoc()) {
$field1name = $row["id"];
$field2name = $row["address"];
$field3name = $row["location"];
$field4name = $row["intrusiondate"];
$field5name = $row["reportingperson"];
$field6name = $row["contactphone"];
$field7name = $row["contactemail"];
echo "<table style='width:100%'>"; // start a table tag in the HTML
				echo '<thead>
								<tr>
																<th>ID</th>
																<th>Address</th>
																<th>Location</th>
																<th>Intrusion Date/Time</th>
																<th>Contact</th>
																<th>Contact Phone</th>
																<th>Contact Email</th>
								</tr>
				</thead>';
				echo '<tbody>
						<tr>
									<td>'.$field1name.'</td>
									<td>'.$field2name.'</td>
									<td>'.$field3name.'</td>
									<td>'.$field4name.'</td>
									<td>'.$field5name.'</td>
									<td>'.$field6name.'</td>
									<td>'.$field7name.'</td>
						</tr>';
			echo "</tbody>";
echo "</table>"; //Close the table in HTML
}
/*freeresultset*/
$result->free();
}
echo "<br>"
?>
<div id="footer">
	
	Copyright &copy; 2019 MAIDS Project - Claudio F. Meis. All Rights Reserved.<br />
Design by Claudio F. Meis</a><br>
<a href="mailto:cfpm@live.ca?Subject=MAIDS%20Intrusion%20Contact">Contact MAIDS</a>
</div>
</body>
</html>
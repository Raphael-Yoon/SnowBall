<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
</head>
<body>
	<form class = "grid" action = "/generate" method = "POST">
	<lable for = "Name">System :</lable>
	<select name="param1">
		<option value="SAP">SAP</option>
		<option value="Oracle">Oracle</option>
		<option value="Douzone">더존</option>
		<option value="KSystem">영림원</option>
		<option value="ETC">ETC</option>
	</select>
	</br>
	<lable for = "Name">OS</lable>
	<select name="param2">
		<option value="Unix">Unix</option>
		<option value="Windows">Windwos</option>
		<option value="Linux">Linux</option>
		<option value="ETC">ETC</option>
	</select>
	</br>
	<lable for = "Name">DB</lable>
	<select name="param3">
		<option value="Oracle">Oracle</option>
		<option value="MSSQL">MS-SQL</option>
		<option value="ETC">ETC</option>
	</select>
	</br>
	<lable for = "Name">공통</lable>
	<input type="checkbox" name="param4" value="common" checked>
	<center><input class="file_submit" type="Submit" value="실행"></center>
	</form>
</body>
</html>
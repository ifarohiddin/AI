<?php

//bazaga ulanish
$db = mysqli_connect("localhost","u9133_salom","Apkuz","u9133_salom");
mysqli_set_charset($db, "utf8mb4");


date_Default_timezone_set("Asia/Tashkent");
$soat=date('H:i');
$soatb=date('H:i', strtotime('1 minutes'));
$result=mysqli_query($db, "SELECT * FROM `sendusers` WHERE `status`='active'"); 
while($row= mysqli_fetch_assoc($result)){
$jv=$row["joriy_vaqt"];   
$mesid=$row["mid"];   
$limit=$row["soni"];   
$status=$row["status"];
$send=$row["send"];
$xturi=$row["holat"];
$nosend=$row["nosend"];
} 
if($soat !=$jv and $soatb !=$jv){
mysqli_query($db, "UPDATE `sendusers` SET `joriy_vaqt`='$soatb'");
}
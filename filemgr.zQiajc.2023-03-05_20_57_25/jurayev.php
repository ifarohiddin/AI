<?php


$och=json_encode([
'inline_keyboard'=>[
 [['text'=>"Orqaga","callback_data"=>"back"]],
]
]);
//bazaga ulanish
$token="7876488844:AAFLtipD2pfKgfESPj1PSCWaF9NAqnzImZM";
$db = mysqli_connect("localhost","u9133_salom","Apkuz","u9133_salom");
mysqli_set_charset($db, "utf8mb4");

$key=json_decode(file_get_contents("key.txt"), true)['message']['reply_markup'];

//daqiqasiga nechta userga xabar jo'natish
$jonatish=600;




date_Default_timezone_set("Asia/Tashkent");
$soat=date('H:i');
$result=mysqli_query($db, "SELECT * FROM sendusers WHERE status='active'"); 
while($row= mysqli_fetch_assoc($result)){
$jv=$row["joriy_vaqt"];   
$creator=$row['creator'];
$mesid=$row["mid"];   
$limit=$row["soni"];   
$status=$row["status"];
$send=$row["send"];
$xturi=$row["holat"];
$type1=$row["type"];
$type2=$row["type2"];
} 
if($soat==$jv){
$res=mysqli_query($db, "SELECT * FROM $type1 LIMIT $limit, $jonatish"); 
while($rowsend= mysqli_fetch_assoc($res)){
$id=$rowsend[$type2];   
$keyurl=file_get_contents("key.txt");
usleep(100000); 
if(strlen($keyurl)<10){
$okk=file_get_contents("https://api.telegram.org/bot$token/$xturi?chat_id=$id&from_chat_id=$creator&message_id=$mesid");
}else{
$okk=file_get_contents("https://api.telegram.org/bot$token/$xturi?chat_id=$id&from_chat_id=$creator&message_id=$mesid&reply_markup=".json_encode($key));
}
$ok=json_decode($okk, true)["ok"];
if($ok){
$results=mysqli_query($db, "SELECT * FROM sendusers"); 
while($row= mysqli_fetch_assoc($results)){
$sd=$row["send"];
}  
$sd+=1;
mysqli_query($db, "UPDATE sendusers SET send='$sd'");
} 
} 
$limit+=$jonatish;
$vt=date('H:i', strtotime("1 minutes"));
mysqli_query($db, "UPDATE sendusers SET joriy_vaqt='$vt'");  
mysqli_query($db, "UPDATE sendusers SET soni='$limit'");  
$rest=mysqli_query($db, "SELECT * FROM $type1 LIMIT $limit, 1"); 
$bor=mysqli_num_rows($rest); 
if($bor==0){
mysqli_query($db, "UPDATE sendusers SET status='passive'");
$result=mysqli_query($db, "SELECT * FROM sendusers WHERE status='passive'"); 
while($row= mysqli_fetch_assoc($result)){
$jv=$row["joriy_vaqt"];   
$bv=$row["boshlash_vaqt"];   
$sn=$row["send"];
} 
$txad=urlencode("Xabar Yuborish Tugatildi! 
Boshlandi: $bv
Tugadi: $jv
Yuborildi: $sn taga");
file_get_contents("https://api.telegram.org/bot$token/sendmessage?chat_id=$creator&text=$txad&parse_mode=html&reply_markup=$och");
unlink("key.txt");
exit();
} 
} 
?>
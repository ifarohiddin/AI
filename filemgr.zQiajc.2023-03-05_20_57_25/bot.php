<?php
ob_start();
error_reporting(0);
date_Default_timezone_set('Asia/Tashkent');

$token="7876488844:AAFLtipD2pfKgfESPj1PSCWaF9NAqnzImZM";

$admin = "5358180855";
$user = "DIYOKING";
$bot = bot('getme',['bot'])->result->username;
$soat = date('H:i');
$sana = date("d.m.Y");


require ("sql.php");


function joinchat($id){
global $mid;
$array = array("inline_keyboard");
$get = file_get_contents("kanal.txt");
$ex = explode("\n",$get);
if($get == null){
return true;
}else{
for($i=0;$i<=count($ex) -1;$i++){
$first_line = $ex[$i];
$first_ex = explode("-",$first_line);
$name = $first_ex[0];
$url = $first_ex[1];
     $ret = bot("getChatMember",[
         "chat_id"=>"@$url",
         "user_id"=>$id,
         ]);
$stat = $ret->result->status;
         if((($stat=="creator" or $stat=="administrator" or $stat=="member"))){
      $array['inline_keyboard']["$i"][0]['text'] = "✅ ". $name;
$array['inline_keyboard']["$i"][0]['url'] = "https://t.me/$url";
         }else{
$array['inline_keyboard']["$i"][0]['text'] = "❌ ". $name;
$array['inline_keyboard']["$i"][0]['url'] = "https://t.me/$url";
$uns = true;
}
}
$array['inline_keyboard']["$i"][0]['text'] = "🔄 Tekshirish";
$array['inline_keyboard']["$i"][0]['callback_data'] = "result";
if($uns == true){
     bot('sendMessage',[
         'chat_id'=>$id,
         'text'=>"⚠️ <b>Botdan foydalanish uchun, quyidagi kanallarga obuna bo'ling:</b>",
'parse_mode'=>html,
'disable_web_page_preview'=>true,
'reply_markup'=>json_encode($array),
]);  
exit();
return false;
}else{
return true;
}
}
}

function bot($method,$datas=[]){
	$url = "https://api.telegram.org/bot5587357372:AAEnynh2yP32Q8IutyBq7K_pXZVO83GEo4k/".$method;
	$ch = curl_init();
	curl_setopt($ch,CURLOPT_URL,$url);
	curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
	curl_setopt($ch,CURLOPT_POSTFIELDS,$datas);
	$res = curl_exec($ch);
	if(curl_error($ch)){
		var_dump(curl_error($ch));
	}else{
		return json_decode($res);
	}
}

$upDate = json_decode(file_get_contents('php://input'));
$message = $upDate->message;
$cid = $message->chat->id;
$name = $message->chat->first_name;
$tx = $message->text;
$mid = $message->message_id;
$type = $message->chat->type;
$text = $message->text;
$uid = $message->from->id;
$id = $message->from->id;
$name = $message->from->first_name;
$familya = $message->from->last_name;
$premium = $message->from->is_premium;
$bio = $message->from->about;
$username = $message->from->username;
$chat_id = $message->chat->id;
$message_id = $message->message_id;
$reply = $message->reply_to_message->text;
$nameru = "<a href='tg://user?id=$uid'>$name $familya</a>";

$caption = $message->caption;
$photo = $message->photo;
$video = $message->video;
$file_id = $video->file_id;
$file_name = $video->file_name;
$file_size = $video->file_size;
$size = $file_size/1000;
$dtype = $video->mime_type;

//inline uchun metodlar
$data = $upDate->callback_query->data;
$qid = $upDate->callback_query->id;
$id = $upDate->inline_query->id;
$query = $upDate->inline_query->query;
$query_id = $upDate->inline_query->from->id;
$cid2 = $upDate->callback_query->message->chat->id;
$mid2 = $upDate->callback_query->message->message_id;
$callfrid = $upDate->callback_query->from->id;
$callname = $upDate->callback_query->from->first_name;
$calluser = $upDate->callback_query->from->username;
$surname = $upDate->callback_query->from->last_name;
$about = $upDate->callback_query->from->about;
$nameuz = "<a href='tg://user?id=$callfrid'>$callname $surname</a>";

$reklama = "kulguch_zona";
$kanal = "Dima_Filma";
$kino = "shaxsiykinochi";


if(in_array($cid,$admin)){
	$admin = $cid;
}

if($text){
$result = mysqli_query($connect,"SELECT * FROM sendusers");
$rew = mysqli_fetch_assoc($result);
if($rew){
}else{
mysqli_query($connect,"INSERT INTO sendusers (mid,soni,boshlash_vaqt,joriy_vaqt,status,send,holat,type,type2,creator) VALUES ('1000','0','00:00','00:00','passive','800','copyMessage','users','user_id','$admin')");
}
}

$res = mysqli_query($connect,"SELECT*FROM user_id WHERE user_id=$cid");
while($a = mysqli_fetch_assoc($res)){
$user_id = $a['user_id'];
$step = $a['step'];
}

if(isset($message)){
	if(!$connect){
		bot('sendMessage',[
		'chat_id'=>$cid,
		'text'=>"⚠️ <b>Xatolik!</b>
		
<i>Baza bilan aloqa mavjud emas!</i>",
		'parse_mode'=>'html',
		]);
		return false;
	}
}

if(isset($message)){
$result = mysqli_query($connect,"SELECT * FROM user_id WHERE user_id = $cid");
$rew = mysqli_fetch_assoc($result);
if($rew){
}else{
mysqli_query($connect,"INSERT INTO user_id(`user_id`,`step`,`sana`) VALUES ('$cid','0','$sana | $soat')");
}
}

if($data == "result"){
bot('deleteMessage',[
'chat_id'=>$cid2,
'message_id'=>$mid2
]);
if(joinchat($cid2)==true){
bot('SendMessage',[
'chat_id'=>$cid2,
'text'=>"<b>Qayta /start bosing.</b>",
'parse_mode'=>'html',
]);
mysqli_query($connect, "UPDATE user_id SET step = '0' WHERE user_id = $cid2");
exit();
}else{
bot('SendMessage',[
'chat_id'=>$cid2,
'text'=>"<b>Qayta /start bosing.</b>",
'parse_mode'=>'html',
]);
exit();
}
}

if($text == "/start" and joinchat($cid)==true){
	bot('sendMessage',[
	'chat_id'=>$cid,
    'text'=>"👋 <b>Salom $name!</b>

<i>Marhamat, kerakli kodni yuboring:</i>",
	'parse_mode'=>'html',
	'reply_markup'=>json_encode([
	'inline_keyboard'=>[
	[['text'=>"🔎 Kodlarni qidirish",'url'=>"https://t.me/$kanal"]]
]
])
]);
mysqli_query($connect, "UPDATE user_id SET step = '0' WHERE user_id = $cid");
exit();
}

if(isset($video)){
if($cid == $admin){
$result = mysqli_query($connect,"SELECT * FROM data WHERE file_name = '$file_name'");
$row = mysqli_fetch_assoc($result);
if(!$row){
$rand = rand(0,9999);
mysqli_query($connect, "INSERT INTO data(`file_name`,`file_id`,`code`) VALUES ('$file_name','$file_id','$rand')");
  $msg = bot('sendMessage',[
      'chat_id'=>"@".$kino."",
      'text'=>"$caption

<b>Kino kodi:</b> <code>$rand</code>

❗️ <b>Diqqat kinoni bot orqali topishingiz mumkin!</b>",
     'parse_mode'=>'html',
     'reply_markup'=>json_encode([
     'inline_keyboard'=>[
[['text'=>"YUKLAB OLISH📥",'url'=>"https://t.me/$bot"]]
]
])
])->result->message_id;
bot('sendMessage',[
	'chat_id'=>$cid,
	'text'=>"<b>Bazaga muvaffaqiyatli joylandi!</b> 

<code>$rand</code>",
	'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
     'reply_markup'=>json_encode([
     'inline_keyboard'=>[
[['text'=>"➡️ @$kino",'url'=>"https://t.me/$kino/$msg"]]
]
])
]);
exit();
}else{
		bot('SendMessage',[
	'chat_id'=>$cid,
	'text'=>"$file_name <b>qabul qilinmadi!</b>

Qayta urinib ko'ring:",
'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}
}
}



if(mb_stripos($text, "/delete") !== false){
if($cid == $admin){
$code = explode(" ", $text)[1];
$res = mysqli_query($connect,"SELECT * FROM data WHERE code = '$code'");
$row = mysqli_fetch_assoc($res);
if(!$row){
	bot('SendMessage',[
	'chat_id'=>$cid,
	'text'=>"$code <b>mavjud emas!</b>

Qayta urinib ko'ring:",
'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}else{
mysqli_query($connect,"DELETE FROM data WHERE code = $code"); 
bot('sendMessage',[
'chat_id'=>$cid,
'text'=>"$code <b>raqamli kino olib tashlandi!</b>",
'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}
}
}



$panel=json_encode([
  'inline_keyboard'=>[
  [['text'=>"📫 Userga Xabar",'callback_data'=>"send"]],
  [['text'=>"📊 Statistika", 'callback_data'=>"stat"]],
  [['text'=>"🗒️ Xabar Xolati", 'callback_data'=>"holat"]],
[['text'=>"🛑 Xabarni toʻxtatish", 'callback_data'=>"off"]],
  ]]);

$orqaga=json_encode([
'inline_keyboard'=>[
[['text'=>"🔄 Orqaga", 'callback_data'=>"back"]],
]
]);

if($data=="holat"){
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
if($row['status']=="passive"){
bot ('answerCallbackQuery', [
'callback_query_id'=> $qid,
'text'=>"Xabar mavjud emas ❗",
'show_alert'=>true,
]);}else{
bot('answercallbackquery',[
'callback_query_id'=>$qid,
'text'=>"📊 Yangilandi",
'show_alert'=>false,
]);
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
$bv=$row["boshlash_vaqt"];   
$sn=$row["send"];
$sh=$row["holat"];
$st=$row["status"];
$st1=$row["type"];
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"<b>🗒️ Xabar xaqida:
🕛 Boshlangan vaqti: $bv
⤴️ Kimga: Userlarga
📤 Yuborildi: $sn ta
⚙️ Xabar turi: $sh
📈 Status: Faol </b>",
'parse_mode'=>'html',
'reply_markup'=>json_encode([
  'inline_keyboard'=>[
  [['text'=>"🔄 Yangilash",'callback_data'=>"gov"],['text'=>"❌ Bosh Menu", 'callback_data'=>"back"]],
  ]])
]); exit();
}
}

if($data=="gov"){
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
if($row['status']=="passive"){
bot ('answerCallbackQuery', [
'callback_query_id'=> $qid,
'text'=>"Xabar mavjud emas ❗",
'show_alert'=>true,
]);}else{
bot('answercallbackquery',[
'callback_query_id'=>$qid,
'text'=>"📊 Yangilandi",
'show_alert'=>false,
]);
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
$bv=$row["boshlash_vaqt"];   
$sn=$row["send"];
$sh=$row["holat"];
$st=$row["status"];
$st1=$row["type"];
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,

'text'=>"<b>🗒️ Xabar xaqida:
🕛 Boshlangan vaqti: $bv
⤴️ Kimga: Userlarga
📤 Yuborildi: $sn ta
⚙️ Xabar turi: $sh
📈 Status: Faol </b>",
'parse_mode'=>'html',
'reply_markup'=>json_encode([
  'inline_keyboard'=>[
  [['text'=>"🔄 Yangilash",'callback_data'=>"holat"],['text'=>"❌ Bosh Menu", 'callback_data'=>"back"]],
  ]])
]); exit();
}
}


if($text=="/panel" and $cid == $admin){
bot('sendMessage',[
'chat_id'=>$cid,
'text'=>"❕Admin Panel ochildi!",'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
'reply_markup'=>$panel,
]);
mysqli_query($connect,"UPDATE user_id SET step ='null' WHERE user_id='$cid'");
exit();
}

if($data=="back"){
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"❗<b>Bosh menu</b>",
'parse_mode'=>'html',
'disable_web_page_preview'=>true,
'reply_markup'=>$panel
]);
mysqli_query($connect,"UPDATE user_id SET step ='null' WHERE user_id='$cid2'");
exit();
}

if($data=="stat"){
$res = mysqli_query($connect, "SELECT * FROM `user_id`");
$us = mysqli_num_rows($res);
$res = mysqli_query($connect, "SELECT * FROM `data`");
$kin = mysqli_num_rows($res);
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"
<b>💥 Faol obunachi: $us ta

➕ Yuklangan kino: $kin ta</b>",
'parse_mode'=>'html',
'disable_web_page_preview'=>true,
'reply_markup'=>$orqaga
]);
mysqli_query($connect,"UPDATE user_id SET step ='null' WHERE user_id='$cid2'");
exit();
}

if($data =="off"){
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"<b>😳 Xabar yuborish toʻxtatilsinmi  </b>",
'parse_mode'=>'html',
'reply_markup'=>json_encode([
  'inline_keyboard'=>[
[['text'=>"⛔ Toʻxtatish", 'callback_data'=>"sendP"]],
[['text'=>"🛑 Orqaga", 'callback_data'=>"back"]],
  ]]),
]); exit ();
}


if($data =="sendP"){
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
if($row['status']=="passive"){
bot ('answerCallbackQuery', [
'callback_query_id'=> $qid,
'text'=>"Xabar mavjud emas ❗",
'show_alert'=>true,
]);exit ();}else{
mysqli_query($connect, "UPDATE sendusers SET status='passive'");
bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"<b>🛑 Muofaqyatli yakunlandi. </b>",
'parse_mode'=>'html',
'reply_markup'=>json_encode([
  'inline_keyboard'=>[
[['text'=>"⛔ Bosh Menu", 'callback_data'=>"back"]],
  ]]),
]); exit ();
}
}


if($data=="send"){
$result=mysqli_query($connect, "SELECT * FROM sendusers"); 
$row= mysqli_fetch_assoc($result);
if($row['status']=="passive"){
	bot('editMessageText',[
'chat_id'=>$cid2,
'message_id'=>$mid2,
'text'=>"❗Userlar uchun <b>Xabarni</b>ni Yuboring.",
'parse_mode'=>'html',
'disable_web_page_preview'=>true,
'reply_markup'=>$orqaga
]);
mysqli_query($connect,"UPDATE user_id SET step ='send' WHERE user_id='$cid2'");exit();
}else{
bot ('answerCallbackQuery', [
'callback_query_id'=> $qid,
'text'=>"Xabar yuborish davom etmoqda❗",
'show_alert'=>true,
]); 
}
}

if($step == "send" and $text !="/start" ){
mysqli_query($connect,"UPDATE user_id SET step ='null' WHERE user_id='$cid'");
$vt=date('H:i', strtotime("1 minutes"));
$soat=date('H:i');
bot('sendmessage',[
'chat_id'=>$cid,
'text'=>"✅ <b>Qabul qildim: $vt da boshlaymiz</b>",
'parse_mode'=>"html",
'reply_markup' =>$orqaga,
]); 
$result=mysqli_query($connect, "SELECT * FROM `sendusers`"); 
$bor=mysqli_num_rows($result);
if($bor>0){
mysqli_query($connect, "UPDATE `sendusers` SET `mid`='$mid', `boshlash_vaqt`='$soat'");  
mysqli_query($connect, "UPDATE `sendusers` SET `soni`='0', `joriy_vaqt`='$vt', `status`='active', `send`='0', `holat`='copyMessage', `type`='user_id', `type2`='user_id',`creator`='$uid'");  
exit();
}else{
mysqli_query($connect, "INSERT INTO `sendusers` (`mid`,`boshlash_vaqt`,`soni`,`joriy_vaqt`,`status`,`send`,`holat`,`type`,`type2`,`creator`) VALUES('$mid', '$vt', 0, '$soat', 'active', 0, 'copyMessage','user_id','user_id','$uid')");
}
$keyb=$upDate->message->reply_markup;
if(isset($keyb)){
file_put_contents("key.txt",file_get_contents('php://input'));
} 
exit();
}

if(isset($text)){
if($text != "/start" and $text != "/stat" and $text != "/send" and $step != "send" and $step != "send-post" and joinchat($cid)==true){
if((mb_stripos($text, "/delete") !== false) and (mb_stripos($text, "/delete") !== false)){
}else{
if(is_numeric($text) == true){
$res = mysqli_query($connect,"SELECT * FROM data WHERE code = '$text'");
$row = mysqli_fetch_assoc($res);
if(!$row){
	bot('SendMessage',[
	'chat_id'=>$cid,
	'text'=>"$text <b>mavjud emas!</b>

Qayta urinib ko'ring:",
'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}else{
$file_name = mysqli_fetch_assoc(mysqli_query($connect,"SELECT*FROM data WHERE code = '$text'"))['file_name'];
$file_id = mysqli_fetch_assoc(mysqli_query($connect,"SELECT*FROM data WHERE code = '$text'"))['file_id'];
      bot('sendVideo',[
      'chat_id'=>$cid,
      'video'=>$file_id,
      'caption'=>"$name
🍿Marhamat tomosha qiling!

🎬Kanalimizga obuna bo'ling👇🏻
@$kanal

@$reklama",
     'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}
}else{
	bot('SendMessage',[
	'chat_id'=>$cid,
	'text'=>"<b>Faqat raqamlardan foydalaning!</b>",
'parse_mode'=>'html',
'reply_to_message_id'=>$mid,
]);
exit();
}
}
}
}


?>
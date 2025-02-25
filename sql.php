<?php

$connect= mysqli_connect("localhost","postgres","Minatokun13.","testdemo");
if($connect){
echo "Ulandi";
}else{
echo "Ulanmadi";
}


?>
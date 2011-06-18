<?php
$mid_primary = $mid_secondary = 220;
$ext_primary = 255;
$ext_secondary = 0;

if ( isset($_GET['v']) )
    $v = $_GET['v'] / 100;
else
    $v = 0.5;

if ( isset($_GET['s']) )
    $scale = $_GET['s'];
else
    $scale = 0;

/* Calculate size */
$size = 15 + min(($scale-500)/3000, 1) * 20;
$img = imagecreatetruecolor($size+1, $size+1);
$black = imagecolorallocate($img, 0, 0, 0);
$trans = imagecolorallocatealpha($img, 0, 255, 0, 127);
imagecolortransparent($img, $trans);
imagefill($img, 0, 0, $trans);
//imagerectangle($img, 0, 0, $size-1, $size-1, $black);


/* Scale colours */
$color_scale = min(abs($v - 0.5) / 0.3, 1);
$primary = $mid_primary + ($ext_primary - $mid_primary) * $color_scale;
$secondary = $mid_secondary + ($ext_secondary - $mid_secondary) * $color_scale;

if ( $v >= 0.5 ) {
    $col = imagecolorallocate($img, $primary, $secondary, $secondary);
}
else {
    $col = imagecolorallocate($img, $secondary, $secondary, $primary);
}

//imagefilledrectangle($img, 1, 1, $size-2, $size-2, $col);
imagefilledellipse($img, $size/2, $size/2, $size, $size, $col);
imageellipse($img, $size/2, $size/2, $size, $size, $black);

header("Content-type: image/png");
imagepng($img);
imagedestroy($img);
?>
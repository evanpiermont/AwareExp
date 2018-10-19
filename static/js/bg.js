

// this code will initilize the screen, font sizes, colors etc. keep colors
// here for easy changing.
//

$base03='#002b36';
$base02='#073642';
$base01='#586e75';
$base00='#657b83';
$base0='#839496';
$base1='#93a1a1';
$base2='#eee8d5';
$base3='#fdf6e3';
$yellow='#b58900';
$orange='#cb4b16';
$red='#dc322f';
$magenta='#d33682';
$violet='#6c71c4';
$blue='#268bd2';
$cyan='#2aa198';
$green='#859900';

$cBG = $base3;
$cInputBG = $base02;
$cInputText = $cyan;
$cBodyText = $base03;
$shape0 = $violet;
$shape1 = $red;
$shape2 = $yellow;
$shape3 = $cyan;

fontsize = function () {
    z = 0.08
    if (window.matchMedia("only screen and (max-width : 500px)").matches) {
        z = 0.11
    }
    var x = $(window).width() * z; // z of container width
    var y = $(window).height() * z; // z of container height
    var fontSize = Math.min(x,y);
    $("body").css('font-size', fontSize);
};



colors = function(){
    $("#background").css('background-color', $cBG);
    $("input").css('background-color', $cInputBG);
    $("input").css('color', $cInputText);
    $("body").css('color', $cBodyText);
    $(".submit").css('background-color', $cInputBG);
};


$(window).resize(fontsize);
$(document).ready(colors);
$(document).ready(fontsize);

window.location.hash="iLSTxs";  
window.location.hash="iLSTxs3";//again because google chrome don't insert first hash into history
window.onhashchange=function(){window.location.hash="iLSTxs";}






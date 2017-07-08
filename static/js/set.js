
//lets populate reel numbers
//

lerp = function(a,b,u) {
        return (1-u) * a + u * b;
};


//
slider = function(){

var $max = 3

var rn = "";
for(var i = 0; i <= 100; i++)
	rn += "<div class=fixedheight>$"+(i*.01*$max).toFixed(2)+"</div>";
$("#rn").html(rn);
$('.fixedheight').css('height', $("#value_bubble").height());



$( '#slider_bdm' ).click( function( ) {
    $('#value_bubble').show();
});


$( '#slider_bdm' ).on( 'input', function( ) {

        var startCBG = {r:38, g:  139, b:  210};  // start color for left hand side of slider.
        var endCBG   = {r:  133, g:153, b:0};  // end color for right hand side
        var alpha = this.value*0.01;
        var r = parseInt(lerp(startCBG.r, endCBG.r, alpha));
        var g = parseInt(lerp(startCBG.g, endCBG.g, alpha));
        var b = parseInt(lerp(startCBG.b, endCBG.b, alpha));
        var colornameCBG = 'rgb('+r+','+g+','+b+')';

        var startCT = {r:181, g:  137, b:  0};  // start color for left hand side of text color.
        var endCT   = {r:  203, g:75, b:22};  // end color for right hand sidie
        var rT = parseInt(lerp(startCT.r, endCT.r, alpha));
        var gT = parseInt(lerp(startCT.g, endCT.g, alpha));
        var bT = parseInt(lerp(startCT.b, endCT.b, alpha));
        var colornameCT = 'rgb('+rT+','+gT+','+bT+')';



        $('#value_bubble').css( 'left', ((this.value - 55)*.98 + 50) + "%" );

        document.getElementById('value_bubble').style.setProperty('background-color', colornameCBG);
        document.getElementById('value_bubble').style.setProperty('border-color', colornameCBG);
        document.getElementById('value_bubble').style.setProperty('color', colornameCT);

        $( this ).css( 'background', 'linear-gradient(to right,' + $blue + ',' + colornameCBG + ' ' + this. value + '%,'+ $green + ')' );

        var v;
        v = this.value*$("#value_bubble").height()*-1 + 'px';
        $("#rn").css({transform: 'translateY('+v+') translateZ(0)'});

});


};




$(document).ready(slider);




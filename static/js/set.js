

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
$cBodyText = $green;
$cOutline = $magenta;


fontsize = function () {
    var x = $(window).width() * 0.10; // 10% of container width
    var y = $(window).height() * 0.10; // 10% of container height
    var fontSize = Math.min(x,y);
    $("body").css('font-size', fontSize);
};

colors = function(){
    $("#background").css('background-color', $cBG);
    $("input").css('background-color', $cInputBG);
    $("input").css('color', $cInputText);
    $("body").css('color', $cBodyText);
};


$(window).resize(fontsize);
$(document).ready(colors);
$(document).ready(fontsize);

window.location.hash="iLSTxs";  
window.location.hash="iLSTxs3";//again because google chrome don't insert first hash into history
window.onhashchange=function(){window.location.hash="iLSTxs";}

$(document).ready(function() { //we need to re aqquire the window sizes
$("#foundsets").scroll(function() {
      
    var $inscroll = document.getElementById("foundsets").scrollTop;
    $('#output-table-header').css('top', $inscroll)   
});
});


renderCard = function(){

    d3.selectAll(".card").each(function() {

    var rect = this.getBoundingClientRect(); // get the bounding rectangle
    var cardW = rect.width;
    var cardH = rect.height;
    var radius = Math.min(cardW,cardH)/8;

    var $pos = [[cardW/5,cardH/2],[cardW/2,cardH/2],[4*cardW/5,cardH/2]]; // defult for #2
    var color = 'green'; // defult for 2

    var cardSpec = $(this).data('card'); //get data for the specification of the cards


    // chagne color accordingly 
    if (cardSpec[0] == 0){
        var color = 'red';
    } else if (cardSpec[0] == 1){
        var color = 'blue';
    }
    // change number accordingly
    if (cardSpec[2] == 0){
        var $pos = [[cardW/2,cardH/2]];
    } else if (cardSpec[2] == 1){
        var $pos = [[3*cardW/8,cardH/2],[5*cardW/8,cardH/2]];
    }

    //render shapes


    if (cardSpec[1] == 0){
        renderTri(this, color, radius, $pos);
    } else if (cardSpec[1] == 1){
        renderSq(this, color, radius, $pos);
    } else if (cardSpec[1] == 2){
        renderCir(this, color, radius, $pos);
    }

});

}

renderCir = function(element, color, radius, pos){

    for (i in pos){

        d3.select(element).append('circle')
                        .attr("cx", pos[i][0])
                        .attr("cy", pos[i][1])
                        .attr("r", radius)
                        .attr('stroke', '#073642')
                        .attr('fill', color)
                        .attr('stroke-width', 2)
    }

}

renderSq = function(element, color, radius, pos){

    for (i in pos){

        d3.select(element).append('rect')
                        .attr("x", pos[i][0]-radius)
                        .attr("y", pos[i][1]-radius)
                        .attr("width", radius*2)
                        .attr("height", radius*2)
                        .attr('stroke', '#073642')
                        .attr('fill', color)
                        .attr('stroke-width', 2)
    }

}

renderTri = function(element, color, radius, pos){

    for (i in pos){

        points = [[pos[i][0],pos[i][1]-radius],[pos[i][0]+(radius*1.2),pos[i][1]+radius],[pos[i][0]-(radius*1.2),pos[i][1]+radius]].join(" ")
        d3.select(element).append('polygon')
                        .attr("points", points)
                        .attr('stroke', '#073642')
                        .attr('fill', color)
                        .attr('stroke-width', 2)
    }

}


$(document).ready(renderCard);


// Create sets function

var clicked = ['card1']


clickCard = function(){

    $(".display_card").click(function() {
        $id = $(this).attr('id');
        var index = clicked.indexOf($id);
        if (index != -1){
            clicked.splice(index, 1);
            $(this).removeClass("clicked");
        } else {
            $(this).addClass("clicked")
            clicked.push($id)
        }

        if (clicked.length > 2){
        var clickedSpec = clicked.map(function(x) {
        return $('#' + x).data('card');
        });
        console.log(clickedSpec);
        isSetThreeCards(clickedSpec);
        }


});

}

$(document).ready(clickCard);


isSetThreeCards = function(cards){

    var result = true
    for (i = 0; i < 3; i++){
        if (( cards[0][i] == cards[1][i] ) && ( cards[0][i] != cards[2][i] )){
            result = false
        }
        else if (( cards[0][i] != cards[1][i] ) && ( cards[0][i] == cards[2][i] )){
            result = false
        }
        else if (( cards[0][i] != cards[1][i] ) && ( cards[1][i] == cards[2][i] )){
            result = false
        }
        }
    console.log(result);
}





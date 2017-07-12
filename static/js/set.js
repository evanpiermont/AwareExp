

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
$shape1 = $red;
$shape2 = $yellow;
$shape3 = $cyan;


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


renderCard = function(object){

    var rect = object.getBoundingClientRect(); // get the bounding rectangle
    var cardW = rect.width;
    var cardH = rect.height;
    var radius = Math.min(cardW,cardH)/8;

    var $pos = [[cardW/5,cardH/2],[cardW/2,cardH/2],[4*cardW/5,cardH/2]]; // defult for #2
    var color = $shape1; // defult for 2

    var cardSpec = $(object).data('card'); //get data for the specification of the cards

    // chagne color accordingly 
    if (cardSpec[0] == 0){
        var color = $shape2;
    } else if (cardSpec[0] == 1){
        var color = $shape3;
    }
    // change number accordingly
    if (cardSpec[2] == 0){
        var $pos = [[cardW/2,cardH/2]];
    } else if (cardSpec[2] == 1){
        var $pos = [[3*cardW/8,cardH/2],[5*cardW/8,cardH/2]];
    }

    //render shapes


    if (cardSpec[1] == 0){
        renderTri(object, color, radius, $pos);
    } else if (cardSpec[1] == 1){
        renderSq(object, color, radius, $pos);
    } else if (cardSpec[1] == 2){
        renderCir(object, color, radius, $pos);
    }

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

renderCards = function(){
    d3.selectAll(".card").each(function() {
        renderCard(this)
    });
}


$(document).ready(renderCards);


// Create sets function

var clicked = [];

function sortNumber(a,b) { //helper function to sort number, we will short the cards by id
    return a - b;
}

clickCard = function(){

    $(".display_card").click(function() {
        $id = $(this).attr('id').slice(4);
        var index = clicked.indexOf($id);
        if (index != -1){
            clicked.splice(index, 1);
            $(this).removeClass("clicked");
        } else {
            $(this).addClass("clicked")
            clicked.push($id)
        }

        if (clicked.length > 2){

        //clicked.sort(sortNumber);

        cardsID = clicked.map(function(x) {
        return $('#card' + x).data('cardid');
        });

        cardsID.sort(sortNumber);


        var clickedSpec = clicked.map(function(x) {
        return $('#card' + x).data('card');
        });

        if (isSetThreeCards(clickedSpec) == false){
            $('#entertextprompt').text("Thats not a set.");
            $('#set_prompt').fadeIn('fast', function(){
                count = 200;
                counter = setInterval(timer, 10)
                timer();
            });
        } else {
            var foundalready = false
            for (var i = 0; i < foundSets.length; i++) {
                if (foundSets[i][0] == cardsID[0] && foundSets[i][1] == cardsID[1] && foundSets[i][2] == cardsID[2]) {
                    foundalready = true;   // Found it
                }
            }
            if (foundalready) {
            $('#entertextprompt').text("You already found that set.");
            $('#set_prompt').fadeIn('fast', function(){
                count = 200;
                counter = setInterval(timer, 10);
                timer();
            });
            } else {
                foundSets.push(cardsID);
                $('#found_count_inuput').val(foundSets.length)
                sendSets(cardsID);
                var clickedSpec = clicked.map(function(x) {
                return '[' + $('#card' + x).data('card')+ ']';
                });
                appendset(clickedSpec);
            }
        }

        $(".display_card").removeClass("clicked");
        clicked = [];
        }


});

}

$(document).ready(clickCard);

var count = 200;
var counter;

function timer(){
    if (count <= 0)
    {
        clearInterval(counter);
        $('#set_prompt').hide();
        document.getElementById('time_penalty').innerHTML=2.00
        return;
     }
     count--;
     document.getElementById('time_penalty').innerHTML=count /100; 
}


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
    return result;
}

// enter sets, send new set of sets


appendset = function(cardsX){
    document.getElementById("output-table").innerHTML +=

        `<tr>
            <td class='foundcard'>
                <svg class='card'  data-card='`+cardsX[0]+`'></svg>
            </td>
            <td class='foundcard'>
                <svg class='card' data-card='`+cardsX[1]+`'></svg>
            </td>
            <td class='foundcard'>
                <svg class='card' data-card='`+cardsX[2]+`'></svg>
            </td>
        </tr>`;

    d3.selectAll("tr .card").each(function() {
        renderCard(this)
    });
       

}

// sends found sets to server, gets json, but right now the json does nothing

sendSets = function(cardsID){
    
    cardsID = JSON.stringify(cardsID);
    formdata = '&cardsX=' + cardsID;
    formdata = formdata += '&subject_id=' + $subject;
    $.post('/_add_set', formdata, function(json){
        console.log(json);
    });
}

// time out the page

pageTimer = function(){
    if (diff_seconds <= 0)
    {
        clearInterval(counter_out);
        document.endform.submit();
        return;
     }
     diff_seconds--;
     document.getElementById('timer').innerHTML=diff_seconds; 
}

var counter_out = setInterval(pageTimer, 1000);

$(document).ready(pageTimer);






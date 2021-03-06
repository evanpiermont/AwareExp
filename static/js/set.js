$(document).ready(function() { //we need to re aqquire the window sizes
$("#foundsets").scroll(function() {
      
    var $inscroll = document.getElementById("foundsets").scrollTop;
    $('#output-table-header').css('top', $inscroll)   
});
});


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
            sendSets(cardsID, false, false, rnd);
            $('#entertextprompt').text("This is not a set.");
            $('#set_prompt').fadeIn('fast', function(){
                count = penalty;
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
            sendSets(cardsID, true, false, rnd);
            $('#entertextprompt').text("You already found that set.");
            $('#set_prompt').fadeIn('fast', function(){
                count = penalty;
                counter = setInterval(timer, 10);
                timer();
            });
            } else {
                foundSets.push(cardsID);
                $('#found_count_inuput').val(foundSets.length)
                sendSets(cardsID, true, true, rnd);
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


function timer(){
    if (count <= 0)
    {
        clearInterval(counter);
        $('#set_prompt').hide();
        document.getElementById('time_penalty').innerHTML=penalty / 100;
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

    var foundnum = $("#output-table").find("tr").length;
    $('#setcount').text(foundnum)
    });
       

}

// sends found sets to server, gets json, but right now the json does nothing

sendSets = function(cardsID,isset,novelset,rnd){
    console.log(rnd)
    cardsX = JSON.stringify(cardsID);
    //issetX = JSON.stringify(isset);
    //novelsetX = JSON.stringify(novelset);
    formdata = '&cardsX=' + cardsX;
    formdata = formdata += '&subject_id=' + $subject;
    formdata = formdata += '&issetX=' + isset;
    formdata = formdata += '&novelsetX=' + novelset;
    formdata = formdata += '&rndX=' + rnd;
    $.post('/_add_set', formdata, function(json){
        console.log(json);
    })
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


// toggle found sets, if mobile

toggleFound = function(){

    $("#toggle").click(function() {
        x = "Show Found Sets"
        y = "Hide Found Sets"
        z = document.getElementById('toggle').innerHTML
        if (z == x){
            $("#foundsets").show()
            document.getElementById('toggle').innerHTML = y
            renderCards()
        } else {
            $("#foundsets").hide()
            document.getElementById('toggle').innerHTML = x
        };
    });
    
}

// check if the page has been visited before

checkTime = function(){
    formdata = '&rndX=' + rnd;
    formdata = formdata += '&subject_id=' + $subject;
    $.post('/_check_time', formdata, function(json){
        console.log(json);
        if (json['reload'] == true){
            window.location.reload(true);
        }
    })
}

$(document).ready(checkTime);

if (window.matchMedia("only screen and (max-width : 500px)").matches) {
        $(document).ready(toggleFound);
    }




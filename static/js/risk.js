
var current_pane=1


$(document).ready(function() { //we need to re aqquire the window sizes
$("#next").click(function() {

	var pane_len = $('.inst').length;
  console.log(pane_len)

		if (current_pane < pane_len) {

      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane+1)).show();
      $('#prev').show();
      renderCards();

      if (current_pane == pane_len - 1) {
        $("#next").text('Submit');
        $("#prev").text('Instructions');
      };

      current_pane+=1; 

  	} else {
        if(document.getElementById("p").innerHTML == "??"){
          alert("You must move the slider.");
        }else{
          $("form[name='risk']").submit();
        };
      };
});

$("#prev").click(function() {


      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane-1)).show();
      renderCards();
      $("#next").text('Next');
      $("#prev").text('Prev');

      current_pane+=(-1); 

  	if (current_pane == 1) {
  		$('#prev').hide();
  	}
});

    document.getElementById("percent").oninput = function() {
      var $perc = this.value
      var $LAl = Math.floor($perc)
      var $CAl = 100 - $LAl
      var $win = "$" + ($LAl/100).toFixed(2) + "*" + $prize_multiplier + " + $" + ($CAl/100).toFixed(2) + " = $" + (($LAl*$prize_multiplier + $CAl)/100).toFixed(2)
      var $lose = "$" + ($CAl/100).toFixed(2)
      document.getElementById("p").innerHTML = $LAl;
      document.getElementById("q").innerHTML = $CAl;
      document.getElementById("win").innerHTML = $win;
      document.getElementById("lose").innerHTML = $lose;
      document.getElementById("checked").classList.add("checked")
      };

});


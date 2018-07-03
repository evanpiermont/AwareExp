
var current_pane=1


$(document).ready(function() { //we need to re aqquire the window sizes
$("#next").click(function() {

	var pane_len = $('.inst').length;

		if (current_pane < pane_len) {

      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane+1)).show();
      $('#prev').show();
      renderCards();

      current_pane+=1; 

  	} else {
  		window.location.replace("/compquiz/"+$subject);
  	}
});

$("#prev").click(function() {


      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane-1)).show();
      renderCards();

      current_pane+=(-1); 

  	if (current_pane == 1) {
  		$('#prev').hide();
  	}
});

});

var current_pane=1


$(document).ready(function() { //we need to re aqquire the window sizes
$("#next").click(function() {

	var pane_len = $('.inst').length;

		if (current_pane < pane_len) {

      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane+1)).show();
      $('#prev').show();
      //renderCards();

      if (current_pane = pane_len - 1) {
        $("#next").text('Submit');
        $("#prev").text('Instructions');
      };

      current_pane+=1; 

  	} else {
      if($('input:radio[name="mpl0"]').is(':checked')){
        $("form[name='risk']").submit();
      };
  	}
});

$("#prev").click(function() {


      $('#pane-'+current_pane).hide();
      $('#pane-'+(current_pane-1)).show();
      //renderCards();
      $("#next").text('Next');
      $("#prev").text('Prev');

      current_pane+=(-1); 

  	if (current_pane == 1) {
  		$('#prev').hide();
  	}
});

$("input:radio").on("click", function() { 

    var $switch = parseInt(this.id.slice(5), 10);
    var $value = this.value
    for (i = 0; i < $switch; i++) { 
        $('[name=mpl'+i+']#L-mpl'+i).prop('checked', true);
      }
    for (i = $switch + 1; i < 11; i++) { 
        $('[name=mpl'+i+']#C-mpl'+i).prop('checked', true);
      }
});

});


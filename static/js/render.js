


renderCard = function(object){

    var rect = object.getBoundingClientRect(); // get the bounding rectangle
    var cardW = rect.width;
    var cardH = rect.height;
    var radius = Math.min(cardW,cardH)/8;

    var $pos = [[cardW/3,cardH/3],[2*cardW/3,cardH/3],[cardW/3,2*cardH/3], [2*cardW/3,2*cardH/3]]; // defult for #3
    var color = $shape3; // defult for 3

    var cardSpec = $(object).data('card'); //get data for the specification of the cards

    // chagne color accordingly 
    if (cardSpec[0] == 0){
        var color = $shape0;
    } else if (cardSpec[0] == 1){
        var color = $shape1;
    } else if (cardSpec[0] == 2){
        var color = $shape2
        ;
    }

    // change number accordingly
    if (cardSpec[2] == 0){
        var $pos = [[cardW/2,cardH/2]];
    } else if (cardSpec[2] == 1){
        var $pos = [[3*cardW/8,cardH/2],[5*cardW/8,cardH/2]];
    } else if (cardSpec[2] == 2){
        var $pos = [[cardW/5,cardH/2],[cardW/2,cardH/2],[4*cardW/5,cardH/2]];
    }

    //render shapes


    if (cardSpec[1] == 0){
        renderTri(object, color, radius, $pos);
    } else if (cardSpec[1] == 1){
        renderSq(object, color, radius, $pos);
    } else if (cardSpec[1] == 2){
        renderCir(object, color, radius, $pos);
    } else if (cardSpec[1] == 3){
        renderStr(object, color, radius, $pos);
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

renderStr = function(element, color, radius, pos){

    for (i in pos){

        points = CalculateStarPoints(pos[i][0], pos[i][1], radius*1.1, radius/2)
        d3.select(element).append('polygon')
                        .attr("points", points)
                        .attr('stroke', '#073642')
                        .attr('fill', color)
                        .attr('stroke-width', 2)
    }

}

function CalculateStarPoints(centerX, centerY, outerRadius, innerRadius)
{
   var results = "";

   var angle = Math.PI / 5;

   for (var i = 0; i < 2 * 5; i++)
   {
      // Use outer or inner radius depending on what iteration we are in.
      var r = (i & 1) == 0 ? outerRadius : innerRadius;
      
      var currX = centerX + Math.cos(i * angle) * r;
      var currY = centerY + Math.sin(i * angle) * r;

      // Our first time we simply append the coordinates, subsequet times
      // we append a ", " to distinguish each coordinate pair.
      if (i == 0)
      {
         results = currX + "," + currY;
      }
      else
      {
         results += ", " + currX + "," + currY;
      }
   }

   return results;
}

renderCards = function(){
    d3.selectAll(".card").each(function() {
        renderCard(this)
    });
}


$(document).ready(renderCards);








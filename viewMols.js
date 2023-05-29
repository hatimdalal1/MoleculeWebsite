$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
      // var slider = document.getElementById("myRange");
      // var output = document.getElementById("demo");
      // output.innerHTML = slider.value; // Display the default slider value

      // // Update the current slider value (each time you drag the slider handle)
      // slider.oninput = function() {
      //   output.innerHTML = this.value;
      // }

      $(".slider").on("change", function(e)
        {
          xval = $("#slideX").val()
          yval = $("#slideY").val()
          zval = $("#slideZ").val()
          molName = $("h4").attr("id")
          coord = $(this).attr("id")
          val = 0
          axis = "x"

          if (coord == "slideX"){
            val = xval
            axis = "x"
          } else if (coord == "slideY"){
            val = yval
            axis = "y"
          } else if (coord == "slideZ") {
            val = zval
            axis = "z"
          }

          console.log(molName, val, axis);

          $.post("/rotation", {
            name: molName,
            value: val,
            coordinate: axis
          }, function (data, status)    //call back function
          {
            $("svg").replaceWith( data  )
          }
          )


        }
      )
        // $.get("/getMols", function(data, status)
        // {
        //     tableBody = document.querySelector('table tbody');
            
        //     console.log("Data: " + data + "\nStatus: " + status);
        //     console.log(jQuery.isPlainObject(data))
        //     console.log(typeof data)

        //     data.forEach(function(item, index){
        //         newRow = document.createElement('tr');
        //         console.log(item, index)
                
        //         newRow.innerHTML = `<td id="molid${item[0]}">${item[0]}</td>`
        //         + `<td class="has-details" id="molname${item[0]}">${item[1]} <span class="details">Num Atoms: ${item[2]}<br>Num Bonds: ${item[3]}</span> </td>`

        //         tableBody.appendChild(newRow);
        //     }
        //     )
        // }
        // )

        // $(".viewButton").click(
        //   function (e)
        //       {
        //       elementID = $(this).attr("id")
        //       eName = $(this).attr("name")
        //       alert(elementID, eName)
        //       $.post("/viewMolecule.html", {
        //           elementName: eName
        //       },
        //       function (data, status)
        //       {
        //           alert( "Element has been deleted" );
        //       }
        //       )
        //   }
        // )

        

         

        
    }
)
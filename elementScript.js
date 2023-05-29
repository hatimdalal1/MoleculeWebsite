
$(document).ready( 
    /* this defines a function that gets called after the document is in memory */
    function()
    {
        // alert("1")
        // $.get("/getElements", function(data, status)
        // {
        //     tableBody = document.querySelector('table tbody');
            
        //     console.log("Data: " + data + "\nStatus: " + status);
        //     console.log(jQuery.isPlainObject(data))
        //     console.log(typeof data)

        //     data.forEach(function(item, index){
        //         newRow = document.createElement('tr');
        //         console.log(item, index)
        //         // item[0] = item[0][0].toUpperCase() + item[0].slice(1).toLowerCase()
        //         // item[1] = item[1][0].toUpperCase() + item[1].slice(1).toLowerCase()
        //         newRow.innerHTML = `<td>${item[0]}</td>`
        //         + `<td>${item[1]}</td>`
        //         + `<td>${item[2]}</td>`
        //         + `<td>${item[3]}</td>`
        //         + `<td>${item[4]}</td>`
        //         + `<td>${item[5]}</td>`
        //         + `<td>${item[6]}</td>`
        //         + `<td> <button type="button" class="deleteButton">X</button> </td>`

        //         tableBody.appendChild(newRow);
        //     }
        //     )
        // }
        // )

        $("form").on("submit",
            function(e)
            {
                // make post req with all the table values from the form
                elementCode = $("#elementCode").val()
                elementCode = elementCode.toLowerCase()
                modCode = elementCode[0].toUpperCase() + elementCode.slice(1);
                console.log(modCode)

                elementName = $("#elementName").val()
                elementName = elementName.toLowerCase()
                modName = elementName[0].toUpperCase() + elementName.slice(1);
                // elementName.charAt(0) = elementName.charAt(0).toUpperCase()
                console.log(modName)
                $.post("/form_handler.html",
                /* pass a JavaScript dictionary */
                {
                    number: $("#elementNum").val(),	/* retreive value of name field */
                    code: modCode,
                    name: modName,
                    c1: $("#colour1").val(),
                    c2: $("#colour2").val(),
                    c3: $("#colour3").val(),
                    radius: $("#radius").val(),
                },
                function( data, status )
                {
                    alert(data);
                }
                )

                // $.get("/getElements", function(data, status)
                // {
                //     tableBody = document.querySelector('table tbody');
            
                //     console.log("Data: " + data + "\nStatus: " + status);
                //     console.log(jQuery.isPlainObject(data))
                //     console.log(typeof data)

                //     data.forEach(function(item, index){
                //         newRow = document.createElement('tr');
                //         console.log(item, index)
                //         newRow.innerHTML = `<td>${item[0]}</td>`
                //         + `<td>${item[1]}</td>`
                //         + `<td>${item[2]}</td>`
                //         + `<td>${item[3]}</td>`
                //         + `<td>${item[4]}</td>`
                //         + `<td>${item[5]}</td>`
                //         + `<td>${item[6]}</td>`

                //         tableBody.appendChild(newRow);
                //     }
                //     )
                // }
                // )
                

                $.get("/addElements.html", function(data, status)
                {
                    var newDoc = document.open("text/html", "replace");
                    newDoc.write(data);
                    newDoc.close();

                    // $('html').replaceWith(data);
                })
                e.preventDefault()
            }
        )

        $(".deleteButton").click(
            function (e)
                {
                elementID = $(this).attr("id")
                $.post("/delete.html", {
                    elementNum: elementID
                },
                function (data, status)
                {
                    alert( "Element has been deleted" );
                }
                )

                $.get("/addElements.html", function(data, status)
                {
                    var newDoc = document.open("text/html", "replace");
                    newDoc.write(data);
                    newDoc.close();

                    // $('html').replaceWith(data);
                })
                e.preventDefault()
            }
        )


    }

)

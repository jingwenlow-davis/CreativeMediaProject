// $(document).ready(function(){
//   $('#q').click(function () {
//
//   // var quotes = $('#quotes');
//   console.log("made it");
//
//   $.ajax({
//     type:"GET",
//     url: "https://talaikis.com/api/quotes/",
//     async: false;
//     dataType: 'json',
//     success: function( data )
//     {
//       console.log(data);
//         // for(i=0; i<; i++){
//         //   $('div').append('<p>'+data[i].quote+</p>);
//         // }
//     }
//   });
//  });
// });



  function updateDB() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "https://talaikis.com/api/quotes/");
    xhttp.addEventListener("load", callback);
    xhttp.send();
  }

  function callback(){
    var data = this.responseText;
    alert(data);
    var quotes = document.getElementById("quotes").value;
    var holdQuote = document.createElement('div');
    var quote = document.createElement('p');
    quote.textContent = data[0].quote;
    holdQuote.append(quote);

  	// invalidQueryDiv.append(invalidQueryPgh);
  	// mainDisplay.append(invalidQueryDiv);
  	// invalidQueryDiv.id = "invalidQ";

  }


// [
// {"quote":"It's really funny because the same people who loved me as Stringer Bell were the same people that were watching 'Daddy's Little Girls' literally in tears.",
//   "author":"Idris Elba",
//   "cat":"funny"
// },
// {"quote":"If I wasn't even famous or had any success, I would still wake up and put tons of make-up on, and put on a cool outfit. That's always been who I've been my whole life, so that's never gonna change. I love fashion. I love getting dressed up. I love Halloween, too.",
//   "author":"Gwen Stefani",
//   "cat":"cool"},
// {"quote":"I don't think the objective of an abortion clinic is to try to talk women out of having the"}

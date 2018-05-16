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
    xhttp.addEventListener("load", callback); // go to callback function
    xhttp.send();
  }

  function callback(){
    var data = JSON.parse(this.responseText); // parse the JSON received from the AJAX
    data = data.slice(0, 10); // get the first 10
    var quotes = document.getElementById("quotes");
var i = 0;
for(i=0; i<10; i++){

      var holdQuote = document.createElement('div'); // div to hold quote (orange box)
      var quote = document.createElement('p'); // p to hold text
      quote.textContent = data[i].quote; // append quote to text
      holdQuote.append(quote);
      quotes.append(holdQuote);
      holdQuote.id = "holdQuote";
    }
  }

  window.onload = updateDB; // call function when page loaded


// <button id="q" onclick="updateDB()">Get JSON data</button>

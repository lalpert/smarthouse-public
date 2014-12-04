var page = require('webpage').create();
page.settings.userName = 'margaret.cunniff@gmail.com';
page.settings.password = 'nytimes'; 

loginUrl = "https://myaccount.nytimes.com/auth/login";

page.onConsoleMessage = function(msg) {
  console.log(msg);
};


login = function(url) {
    page.open(url, function(status) {

        page.evaluate(function() {
          console.log('hello');
          document.getElementById("userid").value = "margaret.cunniff@gmail.com";
          document.getElementById("password").value = "nytimes";
          var btn = document.getElementsByClassName("applicationButton");
          btn.click();
          // page is redirecting.
        });

        setTimeout(function() {
          page.evaluate(function() {
            console.log('haha');
          });
          //phantom.exit();
        }, 5000);
    });
}


parsePage = function(url) {
    page.open(url, function(status) {
        page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", function() {
        
          var title = page.evaluate(function() {
              var squares = $(".grid-square.checked");
              console.log(squares);
              //return squares.length();
              //return document.title;
          });

          console.log('Page title is ' + title);
          //phantom.exit();
        });
    });
}

//url = "http://www.nytimes.com";
url = "http://www.nytimes.com/crosswords/game/2011/11/29/daily/"
parsePage(url);
login(loginUrl);
//phantom.exit();

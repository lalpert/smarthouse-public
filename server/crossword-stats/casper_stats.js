// Run with: casperjs --web-security=false casper_stats.js 
var casper = require('casper').create();
var utils = require('utils');
// This will be symlinked from a private repo
var passwords = require('../passwords.js');
var timeValue;
var numWrong;

Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf())
    dat.setDate(dat.getDate() + days);
    return dat;
}

// Echo any console.log msgs to the terminal
casper.on('remote.message', function(msg) {
    this.echo('remote message caught: ' + msg);
})

// First, log in to the NYT website
loginUrl = "https://myaccount.nytimes.com/auth/login";
casper.start(loginUrl, function() {
    this.echo("started");
    this.fill('form.loginForm', {
        'userid': passwords.email,
        'password': passwords.password,
    }, true);
});

// Print the page title just to show we've submitted the form
casper.thenEvaluate(function(){
   console.log("Page Title: " + document.title);
});

// Scrape crosswords, starting with today and going back 1 day at a time
var numDays = 3;
var count = 0;
console.log("Starting scraping");
casper.repeat(numDays, function() {
    date = new Date();
    date = date.addDays(-1 * count + 1);
    // Format date to YYYY/MM/DD
    month = date.getMonth() + 1;
    if (month < 10) {
        month = "0" + month;
    }
    day = date.getDate();
    if (day < 10) {
        day = "0" + day;
    }
    dateString = date.getFullYear() + "/" + month + "/" + day;
    this.echo("date string " + dateString);
    // Set up next date
    count++;
    // Construct URL
    crosswordUrl = "http://www.nytimes.com/crosswords/game/" + dateString + "/daily/";
    this.echo(crosswordUrl);
    // Open the URL
    casper.thenOpen(crosswordUrl, function() {
        this.echo("Opened crossword");

        // Wait 5 seconds to give everything on page time to load
        this.wait(5000, function() {
            this.echo("I've waited for a second or 5.");
            timeValue = casper.evaluate(function() {
                timerDiv = document.getElementsByClassName("timer-count")[0];
                timeString = timerDiv.innerHTML;
                return timeString;
            });
            numWrong = casper.evaluate(function() {
                checked_list = document.getElementsByClassName('grid-square checked');
                revealed_list = document.getElementsByClassName('grid-square revealed');
                return checked_list.length + revealed_list.length;
            });
            this.echo("time/num " + timeValue + "/" + numWrong);
            complete = casper.evaluate(function() {
                return document.getElementsByClassName("toolbar-complete").length > 0;
            });
            this.echo("complete:" + complete);
            // POST results to server
            if (complete) {
                this.echo("sending ajax");
                casper.open("http://735roosevelt.com/api/crosswords", {
                    method: 'post',
                    data: {
                        "time": timeValue,
                        "num_wrong": numWrong,
                        "date": dateString
                    }
                });
            }
        });
    });
});



    

casper.run();




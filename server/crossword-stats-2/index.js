const puppeteer = require("puppeteer");
const loginUrl = "https://myaccount.nytimes.com/auth/login";
const crosswordBaseUrl = "https://www.nytimes.com/crosswords/game/daily/";

const crosswordUrl = (year, month, day) =>
  `${crosswordBaseUrl}/${year}/${month}/${day}`;
const username = "leah.alpert@gmail.com";
const password = "frog22";
const lazy = "https://www.nytimes.com/crosswords/game/daily/2018/04/05";
const rp = require('request-promise');
/*
<div class="timer-count">14:30</div>
*/
(async () => {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.goto(loginUrl);
  await page.type("#username", username);
  await page.type("#password", password);
  await page.click("#submitButton");
  await page.waitForNavigation();

  const numDays = 7;
  // TODO: handle errors.
  for (let i = 1; i < numDays; i++) {
    await processDay(i, page);
  }
})();

Date.prototype.addDays = function(days) {
  var dat = new Date(this.valueOf());
  dat.setDate(dat.getDate() + days);
  return dat;
};

const processDay = async (daysBack, page) => {
  let date = new Date();
  date = date.addDays(-1 * daysBack + 1);
  // Format date to YYYY/MM/DD
  let month = date.getMonth() + 1;
  if (month < 10) {
    month = "0" + month;
  }
  let day = date.getDate();
  if (day < 10) {
    day = "0" + day;
  }
  const dateString = date.getFullYear() + "/" + month + "/" + day;
  const url = `${crosswordBaseUrl}${dateString}`;
  await page.goto(url);
  const time = await page.evaluate(() => {
    return document.getElementsByClassName("timer-count")[0].innerHTML;
  });
  const numWrong = await page.evaluate(() => {
    return document.getElementsByTagName("use").length;
  });
  const isComplete = (await page.$('[class^="Modal"]')) == null;
  console.log(
    `date is: ${dateString}, time is: ${time}. num wrong: ${numWrong}, is complete: ${isComplete}`
  );
  // TODO: json api
  const options = {
    method: "POST",
    uri: "http://735roosevelt.com/api/crosswords",
    form: {
      time: time,
      num_wrong: numWrong,
      date: dateString
    },
    //json: true // Automatically stringifies the body to JSON
  };
  if (isComplete) {
    await rp(options);
  }
};
/*
loginUrl = "https://myaccount.nytimes.com/auth/login";
casper.start(loginUrl, function() {
    this.echo("started");
    this.fill('form.loginForm', {
        'userid': passwords.email,
        'password': passwords.password,
    }, true);
});
*/

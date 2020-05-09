// init project
const express = require("express"); // the library we will use to handle requests. import it here
const app = express(); // instantiate express
var MongoClient = require("mongodb").MongoClient;
var url = "mongodb://localhost:27017/mydb";
app.use(require("cors")()); // allow Cross-domain requests
app.use(require("body-parser").json()); // When someone sends something to the server, we can recieve it in JSON format

// base route. Responds to GET requests to the root route ('/')
app.get("/", (req, res) => {
  res.send("Home sweet home 🏚"); // always responds with the string "TODO"
});

// base route. Responds to POST requests to the root route
app.post("/", (req, res) => {
  res.send("Sending it through the post 📬"); // always responds with the string "TODO"
});

// Responds to PUT requests to the root route
app.put("/", (req, res) => {
  res.send("Don't you dare put me up to this."); // always responds with the string "TODO"
});

// listen for requests on port 3000
const port = 27017;

// var listener = app.listen(port, "127.0.0.1", () => {
//   console.log("Your app is listening on port " + listener.address().port);
// });

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  console.log("Database created!");
  db.close();
});

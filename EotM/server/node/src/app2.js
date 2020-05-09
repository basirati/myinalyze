const bodyParser = require("body-parser");
const cors = require("cors");
const express = require("express");
const mongoose = require("mongoose");
const morgan = requrie("morgan");
const path = require("path");
import routes from "./routes/api";
// import busboy from './utils/utils';
// const fileupload = require('express-fileupload');
// feature 1 - Vaheh

class App {
  app = express.Application;
  db = mongoose.Connection;

  constructor() {
    this.app = express();
    this.app.use(cors());
    this.db = mongoose.connection;
    this.configure();
    // TODO configure paths
    this.connect()
      .then(() => {
        this.app.listen(3000, () => {
          console.log("listening on port 3000");
        });
      })
      .catch(err => {
        console.log("failed to connect to the database");
        console.log(err);
      });
  }

  configure() {
    this.app.use(bodyParser.urlencoded({ extended: false }));
    this.app.use(bodyParser.json());
    this.app.use(morgan("dev"));
    // const busboytemp = busboy();
    this.app.use(
      "/images",
      express.static(path.join(__dirname, "public", "images"))
    );
    this.app.post("/s", (req, res, next) => {
      res.json("posted");
    });
    // this.app.use('/api', busboytemp);
    this.app.use("/api", routes);
  }

  connect() {
    const mongoDB = "mongodb://mongo:27017/eotm";
    mongoose.connect(mongoDB, { useNewUrlParser: true });
    return new Promise((resolve, reject) => {
      this.db.on("error", err => {
        console.error.bind(console, "error connecting to the database");
        reject(err);
      });
      this.db.once("open", () => {
        resolve();
      });
    });
  }
}

const app = new App();

export default app;

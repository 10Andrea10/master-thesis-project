import express, {Application, Request, Response} from 'express';

const app2 = express();

import {BodyParser} from 'body-parser';

const app = new Express();
// support parsing of application/json type post data
app.use(bodyParser.json());
const port = 3000;
const routes = require('./s rc/routes');
app.use('/', routes);

app.listen(port, () => {
  console.log(`Success! Your application is running on port ${port}.`);
});

// import { makeApp } from "@2aa/fastify-lib";

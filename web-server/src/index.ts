import express, {Express, Request, Response} from 'express';

import BodyParser from 'body-parser';
import {itemsRouter} from './routes';

const app: Express = express();
const port = 3000;

app.use(BodyParser.json());

app.use('/', itemsRouter);

app.listen(port, () => {
  console.log(`[Server]: I am running at https://localhost:${port}`);
});

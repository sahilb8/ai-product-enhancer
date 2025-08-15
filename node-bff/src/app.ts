import express from 'express';
import { productRouter } from './routes/product.route';

const app = express();
app.use(express.json());

app.use(productRouter);

app.listen(3000, () => {
  console.log('started listening on port 3000');
});

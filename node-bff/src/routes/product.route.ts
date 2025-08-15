import express, { Request, Response } from 'express';
import { ProductContoller } from '../controllers/product.controller';

const router = express.Router();
const productContoller = new ProductContoller();

router.post(
  '/product/product-descrition',
  productContoller.getProductDescription,
);

export { router as productRouter };

import express, { Request, Response } from 'express';
import { ProductContoller } from '../controllers/product.controller';

const router = express.Router();
const productContoller = new ProductContoller();

router.post(
  '/product/product-descrition',
  productContoller.getProductDescription,
);

router.post(
  '/product/answer-product-query',
  productContoller.getProductQueryAnswered,
);

export { router as productRouter };

import { Request, Response } from 'express';
import { ProductService } from '../services/product.service';

export class ProductContoller {
  getProductDescription = async (req: Request, res: Response) => {
    try {
      const { productName } = req.body;
      if (!productName) {
        return res.status(400).send({ error: 'productName is required' });
      }
      const productService = new ProductService();
      const productDescription =
        await productService.generateProductDescription(productName);
      res.status(200).send(productDescription);
    } catch (error: unknown) {
      // Log unexpected errors at 'error' level with details of the request
      console.error(
        `Error in ProductContoller (getProductDescription). Input: req.body=${JSON.stringify(
          req.body,
        )}.`,
        error,
      );
      // Send generic error response
      res.sendStatus(500);
    }
  };
}

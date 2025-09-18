import axios from 'axios';

export class ProductService {
  generateProductDescription = async (productName: string) => {
    try {
      const AI_SERVICE_URL = 'http://localhost:8000';

      const productDescription = await axios.post(
        `${AI_SERVICE_URL}/generate-product-description`,
        {
          product_name: productName,
        },
      );

      return productDescription;
    } catch (error: unknown) {
      // Log unexpected errors at 'error' level with details of the request
      console.error(
        `Error in ProductService (generateProductDescription)`,
        error,
      );
    }
  };

  getProductQueryAnswered = async (productQuery: string) => {
    try {
      const AI_SERVICE_URL = 'http://localhost:8000';

      const productQueryAnswer = await axios.post(
        `${AI_SERVICE_URL}/answer-product-query`,
        {
          product_query: productQuery,
        },
      );

      return productQueryAnswer;
    } catch (error: unknown) {
      // Log unexpected errors at 'error' level with details of the request
      console.error(`Error in ProductService (getProductQueryAnswered)`, error);
    }
  };
}

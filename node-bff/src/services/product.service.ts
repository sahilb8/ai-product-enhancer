import axios from 'axios';

export class ProductService {
  generateProductDescription = async (productName: string) => {
    console.log(productName);
    const AI_SERVICE_URL = 'http://localhost:8000';

    const productDescription = await axios.post(
      `${AI_SERVICE_URL}/generate-product-description`,
      {
        product_name: productName,
      },
    );

    return productDescription;
  };
}

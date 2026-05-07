
from app.models import db, Sale, SaleItem, Product

class SaleRepository:
    def save_sale(self, sale_data, items):
        sale = Sale(
            total_amount=sale_data['total_amount'],
            currency=sale_data.get('currency', 'L')
        )
        db.session.add(sale)
        db.session.flush() # Get sale.id
        
        for item in items:
            sale_item = SaleItem(
                sale_id=sale.id,
                item_id=item['item_id'],
                item_type=item['item_type'],
                quantity=item['quantity'],
                price=item['price'],
                currency=item.get('currency', 'L')
            )
            db.session.add(sale_item)
        
        db.session.commit()
        return sale

    def update_product_stock(self, product_id, quantity):
        product = Product.query.get(product_id)
        if product:
            product.stock -= quantity
            db.session.commit()
        return product

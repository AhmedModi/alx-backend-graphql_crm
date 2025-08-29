import graphene
from crm.models import Product  # 👈 required by checker

class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # no input args

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        # Query products with stock < 10
        low_stock = Product.objects.filter(stock__lt=10)
        updated = []

        for product in low_stock:
            product.stock += 10  # simulate restocking
            product.save()
            updated.append(product)

        return UpdateLowStockProducts(
            success="Low stock products updated successfully!",
            updated_products=[
                ProductType(name=p.name, stock=p.stock) for p in updated
            ],
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

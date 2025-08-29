import graphene

class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # no arguments needed

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(self, info):
        # In a real case: query DB for products with stock < 10
        # Here: simulate with dummy products
        products = [
            {"name": "ProductA", "stock": 5},
            {"name": "ProductB", "stock": 8},
        ]
        updated = []
        for p in products:
            if p["stock"] < 10:
                p["stock"] += 10
                updated.append(p)

        return UpdateLowStockProducts(
            success="Low stock products updated successfully!",
            updated_products=[ProductType(**p) for p in updated],
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

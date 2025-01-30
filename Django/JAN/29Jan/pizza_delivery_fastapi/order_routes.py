from fastapi import APIRouter

order_router = APIRouter(prefix="/order")

# This will now be accessible at /order/order
@order_router.get('/')
async def hello():
    return {"message": "Hello from Order!"}
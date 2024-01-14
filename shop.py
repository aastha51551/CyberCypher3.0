from protocols.shopkeeper import foodStock, orderResponse
from protocols.agent import (
    QueryStockRequest,
    QueryStockResponse,
)
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
 
AGENT_ADDRESS = "agent1q2ukr5ult5epwlfpjgtntl68dfn5srtjlnakzw9umvu2useqhga22e3sltk"
 
shopkeeper = Agent(
    name="shopkeeper",
    port=8000,
    seed="shopkeeper secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(shopkeeper.wallet.address())
 
order = QueryStockRequest(  category=3,
    last_order_days=15,)

 
# This on_interval agent function performs a request on a defined period
@shopkeeper.on_interval(period=3.0, messages=QueryStockRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
 
    if not completed:
        await ctx.send(AGENT_ADDRESS, order)
 
@shopkeeper.on_message(QueryStockResponse, replies={foodStock})
async def handle_query_response(ctx: Context, sender: str, msg: QueryStockResponse):
    if len(msg.units) > 0:
        ctx.logger.info("Placing Order Now")
 
        quantity_ordered = msg.units[0]
 
        request = foodStock(
            units=quantity_ordered,
            category=order.category,
            last_order_days=order.last_order_days
        )
 
        await ctx.send(sender, request)
 
 
@shopkeeper.on_message(orderResponse, replies=set())
async def handle_order_response(ctx: Context, _sender: str, msg: orderResponse):
    if msg.success:
        ctx.logger.info("Order Placed Successfully")
 
    ctx.storage.set("completed", True)
 
if __name__ == "__main__":
    shopkeeper.run()
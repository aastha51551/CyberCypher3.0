from protocols.shopinv import invStatus, serviceResponse
from protocols.agentinv import (
    QueryServiceRequest,
    QueryServiceResponse,
)
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
 
AGENT_ADDRESS = "agent1q2ukr5ult5epwlfpjgtntl68dfn5srtjlnakzw9umvu2useqhga22e3sltk"
 
shopkeeperinv = Agent(
    name="shopkeeperinv",
    port=8000,
    seed="shopkeeperinv secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(shopkeeperinv.wallet.address())
 
order = QueryServiceRequest(  serial= 3)

 
# This on_interval agent function performs a request on a defined period
@shopkeeperinv.on_interval(period=3.0, messages=QueryServiceRequest)
async def interval(ctx: Context):
    completed = ctx.storage.get("completed")
 
    if not completed:
        await ctx.send(AGENT_ADDRESS, order)
 
@shopkeeperinv.on_message(QueryServiceResponse, replies={invStatus})
async def handle_query_response(ctx: Context, sender: str, msg: QueryServiceResponse):
    if (msg.success):
        ctx.logger.info("Placing Order Now")
 
        request = invStatus(
            serial=order.serial,
         )
 
        await ctx.send(sender, request)
 
 
@shopkeeperinv.on_message(serviceResponse, replies=set())
async def handle_order_response(ctx: Context, _sender: str, msg: serviceResponse):
    if msg.success:
        ctx.logger.info("Order Placed Successfully")
 
    ctx.storage.set("completed", True)
 
if __name__ == "__main__":
    shopkeeperinv.run()
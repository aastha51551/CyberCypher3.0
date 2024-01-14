from typing import List
 
from uagents import Context, Model, Protocol
from .agent import categoryStatus

class foodStock(Model):
    category: int
    last_order_days: int

class orderResponse(Model):
    units: int
    success: bool

book_proto = Protocol()

@book_proto.on_message(model=foodStock, replies=orderResponse)
async def handle_stock_request(ctx: Context, sender: str, msg: foodStock):
  success=True 
  await ctx.send(sender, orderResponse(success=success))
from typing import List
 
from uagents import Context, Model, Protocol
from .agent import categoryStatus

class foodStock(Model):
    units: int
    category: int
    last_order_days: int

class invStatus(Model):
    category: int
    days: int

class orderResponse(Model):
    success: bool

book_proto = Protocol()

@book_proto.on_message(model=foodStock, replies=orderResponse)
async def handle_stock_request(ctx: Context, sender: str, msg: foodStock):
    units = {
        int(num): categoryStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
    success= True
    
 
    await ctx.send(sender, orderResponse(success=success))
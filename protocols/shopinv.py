from typing import List
 
from uagents import Context, Model, Protocol
from .agentinv import invStatus

class invStatus(Model):
    category: int
    days: int

class serviceResponse(Model):
    success: bool

service_proto = Protocol()

@service_proto.on_message(model=invStatus, replies=serviceResponse)
async def handle_stock_request(ctx: Context, sender: str, msg: invStatus):
  service = {
        int(num): invStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
  for number, status in service.items():
        if (
            status.serial == msg.serial
        ):
            x=number
            break
  instance=service[x]
           
  
  if (
            instance.scale <=5
        ):
            success= True
  if (
            instance.scale>5
        ):
            success = False
  await ctx.send(sender, serviceResponse(success=success))
from typing import List
 
from uagents import Context, Model, Protocol
 
# contains data about inventory status
class invStatus(Model):
    scale: int
    serial : int
 
# contains shopkeeper order request
class QueryServiceRequest(Model):
   serial: int
 
# gives the units to be ordered
class QueryServiceResponse(Model):
    request:bool
 
class GetTotalQueries(Model):
    pass
 
class TotalQueries(Model):
    total_queries: int
query_proto = Protocol()
 
@query_proto.on_message(model=QueryServiceRequest, replies=QueryServiceResponse)
async def handle_query_request(ctx: Context, sender: str, msg: QueryServiceRequest):
    
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
            msg.request= True
  if (
            instance.scale>5
        ):
            msg.request = False
  book=msg.request
  if (msg.request):
   ctx.logger.info(f"Query: {msg}. service booked successfully")
  await ctx.send(sender, QueryServiceResponse(request=book))
  total_queries = int(ctx.storage.get("total_queries") or 0)
  ctx.storage.set("total_queries", total_queries + 1)
 
@query_proto.on_query(model=GetTotalQueries, replies=TotalQueries)
async def handle_get_total_queries(ctx: Context, sender: str, _msg: GetTotalQueries):
    total_queries = int(ctx.storage.get("total_queries") or 0)
    await ctx.send(sender, TotalQueries(total_queries=total_queries))
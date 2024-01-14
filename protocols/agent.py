from typing import List
 
from uagents import Context, Model, Protocol
 
# contains data about each category
class categoryStatus(Model):
    category:int
    demand: int
    stock: int
    freq: int
 
# contains shopkeeper order request
class QueryStockRequest(Model):
    category: int
    last_order_days: int
 
# gives the units to be ordered
class QueryStockResponse(Model):
    units: int
 
class GetTotalQueries(Model):
    pass
 
class TotalQueries(Model):
    total_queries: int
query_proto = Protocol()
 
@query_proto.on_message(model=QueryStockRequest, replies=QueryStockResponse)
async def handle_query_request(ctx: Context, sender: str, msg: QueryStockRequest):
    
  product = {
        int(num): categoryStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
  for number, status in product.items():
        if (
            status.category == msg.category
        ):
            x=number
            break
  instance=product[x]
  diff = instance.stock- instance.demand
  if (diff<=0):
      instance.freq=msg.last_order_days
      unit=instance.stock+ abs(diff)
  if (diff>0): 
      unit= instance.stock-abs(diff)
  ctx.logger.info(f"Query: {msg}. units to be ordered: {unit}.")
  await ctx.send(sender, QueryStockResponse(units=unit))
  total_queries = int(ctx.storage.get("total_queries") or 0)
  ctx.storage.set("total_queries", total_queries + 1)
 
@query_proto.on_query(model=GetTotalQueries, replies=TotalQueries)
async def handle_get_total_queries(ctx: Context, sender: str, _msg: GetTotalQueries):
    total_queries = int(ctx.storage.get("total_queries") or 0)
    await ctx.send(sender, TotalQueries(total_queries=total_queries))
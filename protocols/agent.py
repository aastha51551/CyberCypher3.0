from typing import List
 
from uagents import Context, Model, Protocol
 
class categoryStatus(Model):
    demand: int
    stock: int
    freq: int
 
class QueryStockRequest(Model):
    category: int
    last_order_days: int
 
class QueryStockResponse(Model):
    units: List[int]
 
class GetTotalQueries(Model):
    pass
 
class TotalQueries(Model):
    total_queries: int
query_proto = Protocol()
 
@query_proto.on_message(model=QueryStockRequest, replies=QueryStockResponse)
async def handle_query_request(ctx: Context, sender: str, msg: QueryStockRequest):
    
   units = {
        int(num): categoryStatus(**status)
        for (
            num,
            status,
        ) in ctx.storage._data.items()
        if isinstance(num, int)
    }
   unit=[]
   diff = status.stock- status.demand
   for number, status in units.items():
        if ( diff<0):
         status.freq=msg.last_order_days
         unit.append(int(status.demand))
        if ( diff>0):
         unit.append(int(status.stock))
   ctx.logger.info(f"Query: {msg}. units to be ordered: {unit}.")
   await ctx.send(sender, QueryStockResponse(units=unit))
   total_queries = int(ctx.storage.get("total_queries") or 0)
   ctx.storage.set("total_queries", total_queries + 1)
 
@query_proto.on_query(model=GetTotalQueries, replies=TotalQueries)
async def handle_get_total_queries(ctx: Context, sender: str, _msg: GetTotalQueries):
    total_queries = int(ctx.storage.get("total_queries") or 0)
    await ctx.send(sender, TotalQueries(total_queries=total_queries))
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.shopkeeper import book_proto
from protocols.agent import query_proto, categoryStatus
 
checker = Agent(
    name="checker",
    port=8001,
    seed="checker secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(checker.wallet.address())
 
# build the checker agent from stock protocols
checker.include(query_proto)
checker.include(book_proto)
TABLES = {
    1: TableStatus(seats=2, time_start=16, time_end=22),
    2: TableStatus(seats=4, time_start=19, time_end=21),
    3: TableStatus(seats=4, time_start=17, time_end=19),
}
 
# set the table availability information in the checker protocols
for (number, status) in TABLES.items():
    checker._storage.set(number, status.dict())
 
if __name__ == "__main__":
    checker.run()
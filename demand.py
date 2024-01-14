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
CATEGORIES = {
    1: categoryStatus(demand=10,stock=8,freq=15),
    2: categoryStatus(demand=19,stock=30,freq=20),
    3: categoryStatus(demand=9,stock=12,freq=30),
}
 
for (number, status) in CATEGORIES.items():
    checker._storage.set(number, status.dict())
 
if __name__ == "__main__":
    checker.run()
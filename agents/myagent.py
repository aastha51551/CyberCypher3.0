from uagents import Agent, Context
 
shopkeeper = Agent(
    name="shopkeeper",
    port=8000,
    seed="shopkeeper secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
@shopkeeper.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {ctx.name} and my address is {ctx.address}.")
 
if __name__ == "__main__":
    shopkeeper.run()
from agents import Agent, Runner

agent = Agent(name="Assistant", instructions="You are a helpful assistant.")

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

# Example agent response:
# Functions call themselves,
# Endless loops within loops spin,
# Recursion unfolds.
import os
from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    RunContext,
    cli,
    function_tool,
)
from livekit.plugins import deepgram, google, silero

from rag_knowledge import query_faq

load_dotenv()

# Define the Agent and attach the RAG tool
class CustomerSupportAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=(
                "You are a friendly customer service voice assistant for Apex Cloud Solutions. "
                "Keep your responses concise and natural for voice conversation. "
                "Do not use markdown formatting or emojis in your speech. "
                "Always check company policies using the lookup_company_faq tool when answering questions."
            )
        )

    @function_tool
    async def lookup_company_faq(self, context: RunContext, query: str) -> str:
        """Looks up company policies, refund rules, pricing tiers, and operating hours."""
        return query_faq(query)

# Initialize the server worker
server = AgentServer()

@server.rtc_session()
async def entrypoint(ctx: JobContext):
    # Connect to the incoming caller room
    await ctx.connect()

    # Configure session pipeline: Ears (STT), Brain (Gemini), Voice (TTS)
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=deepgram.STT(),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=deepgram.TTS(model="aura-asteria-en"),
    )

    # Start session with our agent
    await session.start(agent=CustomerSupportAgent(), room=ctx.room)

    # Agent greets caller upon joining
    await session.generate_reply(
        instructions="Greet the caller warmly, mention Apex Cloud Solutions, and ask how you can help."
    )

if __name__ == "__main__":
    cli.run_app(server)
import logfire
from agents import Agent, Runner, WebSearchTool, set_default_openai_client

from app.llm.mcps import get_mcp_servers_context
from app.llm.prompts import INSTRUCTION
from app.llm.tools.github import get_github_repo_content
from app.llm.utils import openai_client

set_default_openai_client(openai_client)


logfire.configure(
    service_name="discord-agent",
    send_to_logfire=False,
)

logfire.instrument_openai_agents()


async def run_agent(message: str, current_conversation: list = None, image_urls: list[str] = None) -> tuple[str, list]:
    async with get_mcp_servers_context() as (active_servers, stack):
        agent = Agent(
            "Devscale AI",
            model="gpt-4.1",
            instructions=INSTRUCTION,
            mcp_servers=active_servers,
            tools=[WebSearchTool(), get_github_repo_content],
        )

        if image_urls:
            content = [{"type": "input_text", "text": message}]
            for image_url in image_urls:
                content.append({"type": "input_image", "image_url": image_url})
            user_input = {"role": "user", "content": content}
        else:
            user_input = {"role": "user", "content": message}

        input_messages = current_conversation or []
        input_messages.append(user_input)

        runner = await Runner.run(agent, input=input_messages)
        chat_messages = runner.to_input_list()

        return runner.final_output, chat_messages

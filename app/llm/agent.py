import logfire
from agents import Agent, Runner, WebSearchTool, set_default_openai_client
from agents.extensions.models.litellm_model import LitellmModel

from app.llm.mcps import get_mcp_servers_context
from app.llm.prompts import INSTRUCTION, get_instruction_with_user_context
from app.llm.tools.github import get_github_repo_content
from app.llm.tools.tavily import tavily_crawl, tavily_scrape, tavily_search
from app.core.settings import settings


logfire.configure(
    service_name="discord-agent",
    send_to_logfire=False,
)

logfire.instrument_openai_agents()


async def run_agent(
    message: str,
    current_conversation: list | None = None,
    image_urls: list[str] | None = None,
    user_id: str | None = None,
    username: str | None = None,
) -> tuple[str, list]:
    async with get_mcp_servers_context() as (active_servers, stack):
        instructions = get_instruction_with_user_context(user_id, username)
        print("insruction", instructions)

        agent = Agent(
            "Devscale AI",
            model=LitellmModel(model=settings.LLM_MODEL, api_key=settings.OPENAI_API_KEY),
            instructions=instructions,
            mcp_servers=active_servers,
            tools=[get_github_repo_content, tavily_search, tavily_crawl, tavily_scrape],
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

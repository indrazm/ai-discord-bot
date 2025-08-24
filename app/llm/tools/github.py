from agents import function_tool
from gitingest import ingest_async


@function_tool
async def get_github_repo_content(url: str) -> tuple[str, str, str]:
    """
    Fetches and processes GitHub repository content using gitingest.

    This function asynchronously ingests a GitHub repository URL and extracts
    comprehensive information about the repository structure and content.

    Args:
        url (str): The GitHub repository URL to process. Should be a valid
        GitHub repository URL (e.g., 'https://github.com/user/repo').

    Returns:
        tuple[str, str, str]: A tuple containing three elements:
            - summary (str): A summary of the repository content and structure
            - tree (str): The directory tree structure of the repository
            - content (str): The actual file contents from the repository

    Raises:
        Exception: May raise exceptions related to network issues, invalid URLs,
        or repository access permissions.
    """
    summary, tree, content = await ingest_async(url)
    return summary, tree, content

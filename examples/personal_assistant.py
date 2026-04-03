from sdk.python.memforge import MemForgeClient


def main() -> None:
    client = MemForgeClient()

    memory = client.add_memory(
        user_id="sdk-user",
        agent_id="sdk-agent",
        content="User likes clean and short answers.",
        memory_type="user_preference",
        summary="Response style preference",
    )
    print("Added memory:", memory.id)

    results = client.search_memory(
        query="short answers",
        user_id="sdk-user",
        agent_id="sdk-agent",
        limit=5,
    )
    print("Search results:", len(results))

    payload = client.recall_for_prompt(
        query="response style",
        user_id="sdk-user",
        agent_id="sdk-agent",
        limit=5,
    )
    print(payload["context_text"])


if __name__ == "__main__":
    main()

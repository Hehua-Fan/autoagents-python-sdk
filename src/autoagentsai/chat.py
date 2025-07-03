from typing import Optional
from client import AutoAgentsClient

class ChatSession:
    def __init__(self, client: AutoAgentsClient):
        self.client = client
        self.chat_id: Optional[str] = None

    def send(self, user_prompt: str) -> str:
        # 拼接上下文
        if self.chat_id:
            history = self.client.get_chat_history(chat_id=self.chat_id)
            context = "\n".join([f"{h['role']}: {h['content']}" for h in history])
            prompt = f"{context}\nuser: {user_prompt}"
        else:
            prompt = user_prompt

        result, new_chat_id = self.client.invoke(prompt=prompt, chat_id=self.chat_id)
        self.chat_id = new_chat_id
        return result.get("choices", [{}])[0].get("content", "")


if __name__ == "__main__":
    client = AutoAgentsClient(
        agent_id="6263ccab9d3742deb7f6dfd7caea6560",
        auth_key="6263ccab9d3742deb7f6dfd7caea6560",
        auth_secret="oKghw8Do8z1BL2A3deqkYWGSouUiFn7y",
        jwt_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiL01Nd1ZDYlRZY2dHWUtCOE1NSVo4dVFHN05BYXYrRlR6Szl3bEQ4bWU0UjQzUldVa2JlWC9CS1VkM3N3ck9ZQmMvYnlUMDc1YzhwRVUzbDdwZ3BGc0l5b0p4L3ZRdXdzS0ozMTZqd0V5RTVBTXFBUXFzcjRwWXF3OHk2WU9PY2dpbVhuenJqOWVOV01hc2tqOFc2b2l3RUFza1pxTUlWUVN6NUxsdE14WHMvV0lGaW1zYjF5RTdpdmR0WGszR0svdHBlTXA1cWdGKzErVGFBNkx1ZDZLK2V0UGQwWkRtWE8vMEZJNGtDaC9zST0iLCJleHAiOjE3NTQxMjk1MzR9.96Q5LOMf8Ve4GCxuOeMW7zISnksGKVLI0UduXQ8RbH8"
    )
    session = ChatSession(client)

    print(session.send("你好"))
    print(session.send("请重复我刚才说的"))
    print(session.send("请告诉我之前都说过什么"))


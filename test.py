from autoagentsai import AutoAgentsClient

client = AutoAgentsClient(
    agent_id="3eea63c71173463580e223e0d565340e",
    auth_key="3eea63c71173463580e223e0d565340e",
    auth_secret="rTjIkV3OjJIfwtp7j0Fa2m6YmCsLvyXr",
)

result = client.invoke("你好")

print(result)
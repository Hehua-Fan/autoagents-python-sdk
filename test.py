from autoagentsai.client import ChatClient

client = ChatClient(
    agent_id="fe91cf3348bb419ba907b1e690143006",
    personal_auth_key="e7a964a7e754413a9ea4bc1395a38d39",
    personal_auth_secret="r4wBtqVD1qjItzQapJudKQPFozHAS9eb"
)

for chunk in client.invoke("你好，请总结文件内容"):
    print(chunk, end="", flush=True)
import uuid
import json
from copy import deepcopy

import requests

from src.autoagentsai import template_registry, api
from src.autoagentsai.graph_models import CreateAppParams


class FlowNode:
    def __init__(self, node_id, module_type, position, inputs=None, outputs=None):
        self.id = node_id
        self.type = "custom"
        self.initialized = False
        self.position = position
        self.data = {
            "inputs": inputs or [],
            "outputs": outputs or [],
            "disabled": False,
            "moduleType": module_type,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "initialized": self.initialized,
            "position": self.position,
            "data": self.data
        }

class FlowEdge:
    def __init__(self, source, target, source_handle="", target_handle=""):
        self.id = str(uuid.uuid4())
        self.type = "custom"
        self.source = source
        self.target = target
        self.sourceHandle = source_handle
        self.targetHandle = target_handle
        self.data = {}
        self.label = ""
        self.animated = False
        self.sourceX = 0
        self.sourceY = 0
        self.targetX = 0
        self.targetY = 0

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "target": self.target,
            "sourceHandle": self.sourceHandle,
            "targetHandle": self.targetHandle,
            "data": self.data,
            "label": self.label,
            "animated": self.animated,
            "sourceX": self.sourceX,
            "sourceY": self.sourceY,
            "targetX": self.targetX,
            "targetY": self.targetY
        }

class FlowGraph:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.viewport = {"x": 0, "y": 0, "zoom": 1.0}

    def add_node(self, node_id, module_type, position, inputs=None, outputs=None):
        tpl = deepcopy(template_registry.NODE_TEMPLATES.get(module_type))
        final_inputs = self.merge_template_io(tpl.get("inputs", []), inputs)
        final_outputs = self.merge_template_io(tpl.get("outputs", []), outputs)
        node = FlowNode(
            node_id=node_id,
            module_type=module_type,
            position=position,
            inputs=final_inputs,
            outputs=final_outputs
        )
        node.data["name"]=tpl.get("name")
        node.data["intro"] = tpl.get("intro")
        if tpl.get("category") is not None:
            node.data["category"] = tpl["category"]
        self.nodes.append(node)

    def add_edge(self, source, target, source_handle="", target_handle=""):
        edge = FlowEdge(source, target, source_handle, target_handle)
        self.edges.append(edge)

    def to_json(self):
        return json.dumps({
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "viewport": self.viewport
        }, indent=2, ensure_ascii=False)

    def set_viewport(self, x, y, zoom):
        self.viewport = {"x": x, "y": y, "zoom": zoom}

    def merge_template_io(self,template_io, custom_io):
        # 参数说明：
        # template_io：模板中inputs或outputs列表，每个元素是一个字段的字典，字段完整
        # custom_io：用户传入的inputs或outputs列表，通常是部分字段，可能只有部分key覆盖

        if not custom_io:
            # 如果用户没有传自定义字段，直接返回模板的完整字段（深拷贝避免修改原数据）
            return deepcopy(template_io)

        merged = []
        # 遍历模板里的所有字段
        for t_item in template_io:
            # 在用户自定义列表中找有没有和当前模板字段 key 一样的字段
            c_item = next((c for c in custom_io if c.get("key") == t_item.get("key")), None)

            if c_item:
                # 找到了用户自定义字段
                merged_item = deepcopy(t_item)  # 先复制模板字段（保证完整结构）
                merged_item.update(c_item)  # 用用户的字段内容覆盖模板字段（例如value、description等被覆盖）
                merged.append(merged_item)
            else:
                # 用户没定义，直接用模板字段完整拷贝
                merged.append(deepcopy(t_item))

        return merged

    def post_with_jwt(self, personal_auth_key: str, personal_auth_secret: str, data: CreateAppParams, base_url: str = "https://uat.agentspro.cn") -> requests.Response:
        # 获取 JWT Token，假设get_jwt_token_api需要这两个参数
        jwt_token = api.get_jwt_token_api(personal_auth_key, personal_auth_secret,base_url)

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        url=f"{base_url}/api/agent/create"
        data.appModel=self.to_json()
        if not data.name:
            data.name = "test"
        response = requests.post(url, json=data.model_dump(), headers=headers)
        # 判断请求结果
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("code") == 1:
                # 成功，返回接口响应内容（包含知识库ID等信息）
                print("创建成功")
                return response_data
            else:
                raise Exception(f"创建智能体失败: {response_data.get('msg', 'Unknown error')}")
        else:
            raise Exception(f"创建智能体失败: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # graph = FlowGraph()
    #
    # graph.add_node(node_id="agent1", module_type="questionInput", position={"x": 0, "y": 100})
    # # graph.add_node(node_id="agent2", module_type="httpInvoke", position={"x": 300, "y": 100})
    # graph.add_node(node_id="agent3", module_type="aiChat", position={"x": 300, "y": 100})
    #
    # graph.add_edge(source="agent1", target="agent3", source_handle="userChatInput", target_handle="text")
    #
    # # 导出为 JSON 请求体
    # print(graph.to_json())

    graph = FlowGraph()

    # 添加用户提问节点
    graph.add_node(
        node_id="question1",
        module_type="questionInput",
        position={"x": 0, "y": 100},
    )


    print(graph.to_json())

    graph.post_with_jwt("135c9b6f7660456ba14a2818a311a80e","i34ia5UpBnjuW42huwr97xTiFlIyeXc7",data=CreateAppParams())
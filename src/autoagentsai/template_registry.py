from copy import deepcopy

NODE_TEMPLATES = {
    "httpInvoke": {
        "name": "HTTP调用",
        "intro": "1、发出一个HTTP请求，实现与其他应用服务的数据请求操作。\n\n2、可实现如搜索，数据库信息检索等复杂操作。",
        "category": "HTTP操作",
        "moduleType": "httpInvoke",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "url",
                "type": "textarea",
                "label": "请求地址",
                "value": "post(可选get,post,delete,put,patch) https://xxx\ndata-type json(可选json,form,query) \ntoken xxx\nheader2Key header2Value",
                "connected": False,
                "valueType": "string",
                "description": "输入目标请求链接"
            },
            {
                "key": "_requestBody_",
                "type": "target",
                "label": "全部请求参数",
                "connected": True,
                "valueType": "string",
                "description": "输入POST请求体完整的JSON数据"
            }
        ],
        "outputs": [
            {
                "key": "_success_",
                "type": "source",
                "label": "请求成功",
                "targets": [],
                "valueType": "boolean",
                "description": "http请求成功"
            },
            {
                "key": "_failed_",
                "type": "source",
                "label": "请求异常",
                "targets": [],
                "valueType": "boolean",
                "description": "http请求异常"
            },
            {
                "key": "_response_",
                "type": "source",
                "label": "请求结果",
                "targets": [],
                "valueType": "string",
                "description": "http请求返回的全部结果数据"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "请求完成后触发"
            }
        ]
    },
    "questionInput": {
        "name": "用户提问",
        "intro": "用户输入入口,对话中用户的输入信息,与其他模块连接,一般作为起始模块",
        "category": "用户提问",
        "moduleType": "questionInput",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "inputText",
                "type": "switch",
                "label": "输入文本",
                "value": True,
                "valueType": "boolean",
                "description": "输入文本开关"
            },
            {
                "key": "uploadFile",
                "type": "switch",
                "label": "上传文档",
                "value": False,
                "valueType": "boolean",
                "description": "上传文档开关"
            },
            {
                "key": "uploadPicture",
                "type": "switch",
                "label": "上传图片",
                "value": False,
                "valueType": "boolean",
                "description": "上传图片开关"
            },
            {
                "key": "fileUpload",
                "type": "switch",
                "label": "文档审查",
                "value": False,
                "valueType": "boolean",
                "description": "文档审查开关"
            },
            {
                "key": "fileContrast",
                "type": "checkBox",
                "label": "是否文档对比",
                "value": False,
                "valueType": "boolean",
                "description": "是否开启文档比对功能"
            },
            {
                "key": "fileInfo",
                "type": "table",
                "label": "文档分组",
                "value": [],
                "valueType": "any",
                "description": "上传的文件列表,如果开启了文档对比,每个分组只能上传一个文件"
            },
            {
                "key": "initialInput",
                "type": "hidden",
                "label": "是否作为初始全局input",
                "value": True,
                "valueType": "boolean",
                "description": "是否作为初始全局input"
            }
        ],
        "outputs": [
            {
                "key": "userChatInput",
                "type": "source",
                "label": "文本信息",
                "targets": [],
                "valueType": "string",
                "description": "引用变量：{{userChatInput}}"
            },
            {
                "key": "files",
                "type": "source",
                "label": "文档信息",
                "targets": [],
                "valueType": "file",
                "description": "以JSON数组格式输出用户上传文档列表，若为文档比对，包含分组信息"
            },
            {
                "key": "images",
                "type": "source",
                "label": "图片信息",
                "targets": [],
                "valueType": "image",
                "description": "以JSON数组格式输出用户上传的图片列表"
            },
            {
                "key": "unclickedButton",
                "type": "source",
                "label": "未点击按钮",
                "targets": [],
                "valueType": "boolean",
                "description": "当未点击任何按钮时值为true"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后开关打开,下游链接组件开始运行。"
            }
        ]
    },
    "aiChat": {
        "name": "智能对话",
        "intro": "AI 对话模型，根据信息输入和提示词（Prompt）加工生成所需信息，展示给用户，完成与用户互动。",
        "category": "大模型",
        "moduleType": "aiChat",
        "inputs": [
            {
                "key": "switch",
                "type": "target",
                "label": "联动激活",
                "value": False,
                "keyType": "trigger",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游所有条件方可激活当前组件执行逻辑"
            },
            {
                "key": "switchAny",
                "type": "target",
                "label": "任一激活",
                "value": False,
                "keyType": "triggerAny",
                "connected": True,
                "valueType": "boolean",
                "description": "同时满足上游任一条件即可激活当前组件执行逻辑"
            },
            {
                "key": "text",
                "type": "target",
                "label": "信息输入",
                "value": "",
                "connected": True,
                "valueType": "string",
                "description": "引用变量：{{text}}"
            },
            {
                "key": "images",
                "type": "target",
                "label": "图片输入",
                "value": "",
                "connected": True,
                "valueType": "image",
                "description": "引用变量：{{images}}"
            },
            {
                "key": "knSearch",
                "type": "target",
                "label": "知识库搜索结果",
                "value": "",
                "connected": True,
                "valueType": "search",
                "description": "引用变量：{{knSearch}}"
            },
            {
                "key": "knConfig",
                "type": "target",
                "label": "知识库高级配置",
                "value": "...",
                "connected": False,
                "valueType": "text",
                "description": "知识库高级配置"
            },
            {
                "key": "historyText",
                "type": "inputNumber",
                "label": "聊天上下文",
                "value": 3,
                "min": 0,
                "max": 6,
                "step": 1,
                "connected": False,
                "valueType": "chatHistory",
                "description": ""
            },
            {
                "key": "model",
                "type": "selectChatModel",
                "label": "选择模型",
                "value": "glm-4-airx",
                "required": True,
                "valueType": "string",
                "description": ""
            },
            {
                "key": "quotePrompt",
                "type": "textarea",
                "label": "提示词 (Prompt)",
                "value": "请模拟成AI智能助手...",
                "valueType": "string",
                "description": "模型引导词"
            },
            {
                "key": "stream",
                "type": "switch",
                "label": "回复对用户可见",
                "value": True,
                "connected": False,
                "valueType": "boolean",
                "description": "控制回复内容是否输出给用户"
            },
            {
                "key": "temperature",
                "type": "slider",
                "label": "回复创意性",
                "value": 0,
                "min": 0,
                "max": 1,
                "step": 0.1,
                "markList": {
                    "0": "严谨",
                    "1": "创意"
                },
                "valueType": "number",
                "description": "控制回复创意性"
            },
            {
                "key": "maxToken",
                "type": "slider",
                "label": "回复字数上限",
                "value": 3000,
                "min": 100,
                "max": 5000,
                "step": 50,
                "markList": {
                    "100": "100",
                    "5000": "5000"
                },
                "valueType": "number"
            }
        ],
        "outputs": [
            {
                "key": "isResponseAnswerText",
                "type": "source",
                "label": "回复结束",
                "targets": [],
                "valueType": "boolean",
                "description": "模型运行结束后触发"
            },
            {
                "key": "answerText",
                "type": "source",
                "label": "回复内容",
                "targets": [],
                "valueType": "string",
                "description": "大模型返回结果"
            },
            {
                "key": "finish",
                "type": "source",
                "label": "模块运行结束",
                "targets": [],
                "valueType": "boolean",
                "description": "运行完成后触发"
            }
        ]
    }
}

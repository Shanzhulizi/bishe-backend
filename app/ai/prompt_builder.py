from typing import List, Dict


def build_system_prompt(character, content: str, history: List[Dict] = None) -> List[Dict]:
    system_msg = f"""你正在扮演一个角色，请完全沉浸在这个角色中。

    角色名称：{character.name}
    角色简介：{character.description}
    角色设定：{character.worldview}

    重要要求：
    1. 请始终以 {character.name} 的身份思考和回应
    2. 不要提及你是AI或助手
    3. 保持角色设定的一致性
    4. 对话风格要符合角色特点
    
    现在开始角色扮演，以下是用户的最新消息：
    用户消息：{content}
    以下是与你的对话历史：
    
    """
    messages = [{"role": "system", "content": system_msg}]

    # 2️⃣ 添加历史消息（如果有）
    if history:
        messages.extend(history)

    return messages

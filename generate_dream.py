#!/usr/bin/env python3
"""
AI梦境生成脚本
自动从维基百科获取种子词汇，使用DeepSeek生成梦境文本，
使用通义千问生成图像提示和梦境图像
"""

import os
import json
import requests
import datetime
import random
import time
from pathlib import Path

# 配置API密钥 - 优先从环境变量读取，如果没有则从.env文件读取
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
TONGYI_API_KEY = os.getenv("TONGYI_API_KEY")

# 如果环境变量中没有，尝试从.env文件读取
if not DEEPSEEK_API_KEY or not TONGYI_API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
        TONGYI_API_KEY = os.getenv("TONGYI_API_KEY")
    except ImportError:
        pass

# 检查API密钥是否存在
if not DEEPSEEK_API_KEY:
    raise ValueError("错误: DEEPSEEK_API_KEY 未设置。请在环境变量或.env文件中配置。")
if not TONGYI_API_KEY:
    raise ValueError("错误: TONGYI_API_KEY 未设置。请在环境变量或.env文件中配置。")

# API端点
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
TONGYI_CHAT_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
TONGYI_IMAGE_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"

# 中文词汇来源API - 使用中文维基百科随机页面
WIKIPEDIA_API_URL = "https://zh.wikipedia.org/api/rest_v1/page/random/summary"

def get_wikipedia_seeds(num_seeds=5):
    """从维基百科获取随机文章标题作为种子词汇（备用方案）"""
    seeds = []
    for _ in range(num_seeds):
        try:
            response = requests.get(WIKIPEDIA_API_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', '')
                # 提取名词（简单处理：取标题中的主要词汇）
                words = title.split()
                if words:
                    seeds.append(words[0].lower())
        except Exception as e:
            print(f"获取维基百科种子时出错: {e}")
            continue
    
    # 如果获取失败，使用中文备用词汇
    if not seeds:
        backup_seeds = ["梦境", "幻想", "记忆", "幻象", "幻觉", "星辰", "海洋", "森林", "天空", "时间"]
        seeds = random.sample(backup_seeds, min(num_seeds, len(backup_seeds)))
    
    return seeds[:num_seeds]

def generate_dream_seeds(num_seeds=5):
    """使用DeepSeek生成合理的梦境种子词汇"""
    prompt = f"""请生成{num_seeds}个适合用于梦境创作的中文词汇。
要求：
1. 词汇要富有想象力、梦幻、超现实
2. 适合用于AI生成梦境文本
3. 词汇之间要有一定的关联性和美感
4. 每个词汇2-4个汉字
5. 输出格式：直接输出词汇，用逗号分隔

例如：星辰, 海洋, 记忆, 幻影, 时光"""
    
    result = call_deepseek_api(prompt, max_tokens=100)
    
    if result:
        try:
            # 清理结果，提取词汇
            seeds = [seed.strip() for seed in result.split(',')]
            seeds = [seed for seed in seeds if 2 <= len(seed) <= 4 and not any(char.isdigit() for char in seed)]
            
            if len(seeds) >= num_seeds:
                return seeds[:num_seeds]
            else:
                print(f"DeepSeek生成的词汇不足{num_seeds}个，使用备用方案")
                return get_wikipedia_seeds(num_seeds)
        except Exception as e:
            print(f"处理DeepSeek生成的词汇时出错: {e}")
            return get_wikipedia_seeds(num_seeds)
    else:
        print("DeepSeek生成词汇失败，使用备用方案")
        return get_wikipedia_seeds(num_seeds)

def call_deepseek_api(prompt, max_tokens=500):
    """调用DeepSeek API生成文本"""
    # 清理API密钥，移除可能的引号或空格
    api_key = DEEPSEEK_API_KEY.strip().strip('"').strip("'")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.8
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"DeepSeek API错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"调用DeepSeek API时出错: {e}")
        return None

def call_tongyi_chat_api(prompt, max_tokens=300):
    """调用通义千问聊天API"""
    # 清理API密钥，移除可能的引号或空格
    api_key = TONGYI_API_KEY.strip().strip('"').strip("'")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "qwen-max",
        "input": {
            "messages": [{"role": "user", "content": prompt}]
        },
        "parameters": {
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(TONGYI_CHAT_API_URL, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['output']['text'].strip()
        else:
            print(f"通义千问聊天API错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"调用通义千问聊天API时出错: {e}")
        return None

def call_tongyi_image_api(prompt):
    """调用通义千问图像生成API（异步方式）"""
    # 清理API密钥，移除可能的引号或空格
    api_key = TONGYI_API_KEY.strip().strip('"').strip("'")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 启用异步调用
    }
    
    payload = {
        "model": "wan2.2-t2i-flash",
        "input": {
            "prompt": prompt
        },
        "parameters": {
            "style": "<auto>",  # 使用<auto>风格，通义千问支持
            "size": "1024*1024",  # 通义千问使用*而不是x
            "n": 1
        }
    }
    
    try:
        # 第一步：创建异步任务
        response = requests.post(TONGYI_IMAGE_API_URL, json=payload, headers=headers, timeout=60)
        if response.status_code == 200:
            result = response.json()
            task_id = result['output']['task_id']
            print(f"图像生成任务已创建，任务ID: {task_id}")
            
            # 第二步：轮询任务状态
            task_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
            max_attempts = 30  # 最多尝试30次
            wait_time = 2      # 每次等待2秒
            
            for attempt in range(max_attempts):
                time.sleep(wait_time)
                task_response = requests.get(task_url, headers=headers, timeout=30)
                
                if task_response.status_code == 200:
                    task_result = task_response.json()
                    # 调试输出，查看完整的响应结构
                    print(f"任务响应: {json.dumps(task_result, ensure_ascii=False)[:200]}...")
                    
                    task_status = task_result['output']['task_status']
                    
                    if task_status == 'SUCCEEDED':
                        # 通义千问的响应结构可能有变化，需要灵活处理
                        if 'results' in task_result['output'] and task_result['output']['results']:
                            image_url = task_result['output']['results'][0]['url']
                        elif 'task_result' in task_result['output'] and 'image_urls' in task_result['output']['task_result']:
                            image_url = task_result['output']['task_result']['image_urls'][0]
                        else:
                            print("无法找到图像URL")
                            return None
                            
                        # 下载图像
                        image_response = requests.get(image_url, timeout=30)
                        if image_response.status_code == 200:
                            return image_response.content
                        else:
                            print(f"下载图像时出错: {image_response.status_code}")
                            return None
                    elif task_status == 'FAILED':
                        error_msg = task_result['output'].get('message', '未知错误')
                        print(f"图像生成任务失败: {error_msg}")
                        return None
                    # 如果任务还在处理中，继续等待
                    print(f"任务处理中... ({attempt + 1}/{max_attempts})")
                else:
                    print(f"查询任务状态失败: {task_response.status_code}")
                    return None
            
            print("图像生成超时")
            return None
        else:
            print(f"通义千问图像API错误: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"调用通义千问图像API时出错: {e}")
        return None

def generate_dream_text(seeds):
    """生成梦境文本"""
    seed_str = ", ".join(seeds)
    prompt = f"""请基于以下词汇创作一段超现实的梦境描述（100-150字）：
{seed_str}

要求：
1. 风格超现实、梦幻、富有想象力
2. 语言优美流畅，充满诗意
3. 将这些词汇自然地融入梦境场景中
4. 保持神秘和梦幻的氛围
5. 用中文写作

请直接输出梦境描述，不要添加任何解释或标记。"""

    return call_deepseek_api(prompt)

def generate_image_prompt(dream_text):
    """根据梦境文本生成图像提示"""
    prompt = f"""请将以下梦境描述转化为一个适合AI图像生成的英文提示词：

{dream_text}

要求：
1. 输出纯英文的提示词
2. 包含丰富的视觉细节和艺术风格描述
3. 适合用于文生图模型
4. 包含超现实主义、梦幻的艺术风格
5. 长度在50-100个英文单词之间

请直接输出提示词，不要添加任何解释或标记。"""

    return call_tongyi_chat_api(prompt)

def main():
    """主函数：生成完整的梦境记录"""
    print("开始生成AI梦境...")
    
    # 1. 获取种子词汇
    seeds = generate_dream_seeds(5)
    print(f"种子词汇: {seeds}")
    
    # 2. 生成梦境文本
    dream_text = generate_dream_text(seeds)
    if not dream_text:
        print("生成梦境文本失败")
        return False
    print(f"梦境文本生成成功: {dream_text[:50]}...")
    
    # 3. 生成图像提示
    image_prompt = generate_image_prompt(dream_text)
    if not image_prompt:
        print("生成图像提示失败")
        return False
    print(f"图像提示生成成功: {image_prompt[:50]}...")
    
    # 4. 生成梦境图像
    image_data = call_tongyi_image_api(image_prompt)
    if not image_data:
        print("生成梦境图像失败")
        return False
    print("梦境图像生成成功")
    
    # 5. 准备数据
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    dream_data = {
        "date": today,
        "seeds": seeds,
        "text": dream_text,
        "image_prompt": image_prompt,
        "image_path": f"assets/images/{today}.png"
    }
    
    # 6. 保存图像
    assets_dir = Path("assets/images")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    image_path = assets_dir / f"{today}.png"
    with open(image_path, "wb") as f:
        f.write(image_data)
    
    # 7. 更新数据文件
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    dreams_file = data_dir / "dreams.json"
    dreams = []
    
    if dreams_file.exists():
        with open(dreams_file, "r", encoding="utf-8") as f:
            try:
                dreams = json.load(f)
            except json.JSONDecodeError:
                dreams = []
    
    # 将新梦境插入到数组开头
    dreams.insert(0, dream_data)
    
    # 保存更新后的数据
    with open(dreams_file, "w", encoding="utf-8") as f:
        json.dump(dreams, f, ensure_ascii=False, indent=2)
    
    print(f"梦境记录已保存: {today}")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

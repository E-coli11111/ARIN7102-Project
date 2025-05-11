import openai
import json
import asyncio
import os
from typing import Dict
import aiofiles
import time
import pandas as pd

# name_ref = pd.read_csv("crawling/annual_report.csv")

# 初始化OpenAI客户端
client = openai.AsyncOpenAI(
    api_key=os.getenv("API_KEY", ""),
    base_url=os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
)

# Limit the number of concurrent requests
RATE_LIMIT = 5  
semaphore = asyncio.Semaphore(RATE_LIMIT)

async def generate_keywords_system_prompt() -> str:
    """Produce system prompt (keep synchronous function)"""
    return """
    You are a professional ESG analyst. You should complete the following tasks:
    
    1. Extract keywords from the provided annual report. Focus on the most relevant ESG-related keywords.
    2. Extract performance measurement metrics related to ESG.
    
    Requirements:
    - Output JSON format:
      {
        "keywords": ["keyword1", "keyword2", ...],
        "metrics": ["metric1", "metric2", ...]
      }
    - Keywords must be:
        - Noun phrases, lowercase, full terms
        - Exclude generic terms
    - Metrics must be:
        - ESG-related performance measurement metrics
        - Short noun phrases, no more than 3 words
        - Exclude generic terms
    - Minimum 5 keywords and 3 metrics
    """

async def validate_keywords(data: Dict) -> bool:
    """Validate data structure asynchronously"""
    required_keys = {"keywords", "metrics"}
    if not all(key in data for key in required_keys):
        return False
    return len(data["keywords"]) >= 5 and len(data["metrics"]) >= 3

async def extract_keywords_llm(text: str, filename: str, max_retries=3) -> Dict:
    """Keyword extraction using LLM asynchronously"""
    # name = name_ref[name_ref["company_name"] == filename.split("\\")[1]]["name"].values[0]
    system_prompt = await generate_keywords_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Report Content:\n{text}"}  
    ]
    
    for attempt in range(max_retries):
        try:
            # 使用 Semaphore 限制并发请求
            async with semaphore:
                response = await client.chat.completions.create(
                    model="qwen-long",
                    messages=messages,
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
            
            result = json.loads(response.choices[0].message.content)
            # result["name"] = name
            
            if await validate_keywords(result):
                return result
            raise ValueError("Validation failed")
            
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {filename}: {str(e)}")
            await asyncio.sleep(2 ** attempt) 
            
    return {"keywords": [], "metrics": []}

async def process_file(filepath: str, output_path: str):
    """Process a single file asynchronously"""
    try:
        print(f"Processing {filepath}...")
        async with aiofiles.open(filepath, "r", encoding="utf-8") as f:
            text = await f.read()
            
        result = await extract_keywords_llm(text, filepath)
        
        async with aiofiles.open(output_path, "a", encoding="utf-8") as f:
            await f.write(json.dumps(result, ensure_ascii=False) + "\n")
            
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")

async def main():
    input_dir = "data"
    output_path = "keyword/keywords.jsonl"
    
    # Output path
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    tasks = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                tasks.append(process_file(filepath, output_path))
                
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)
    
    print("Processing completed")

if __name__ == "__main__":
    asyncio.run(main())
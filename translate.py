import openai
from langdetect import detect
import os
from dotenv import load_dotenv

# Tải các biến môi trường từ file .env
load_dotenv()

# Thiết lập khóa OpenAI API
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Định nghĩa kho thuật ngữ
TERMINOLOGY = {
"massive MIMO": "đa đầu vào đa đầu ra quy mô lớn",
"beamforming": "tạo chùm tia",
"5G network": "mạng 5G"
}
def translate_text(input_text, target_language="zh"):
    """Hàm dịch đa ngôn ngữ, có hiệu chỉnh thuật ngữ"""
    # Phát hiện ngôn ngữ đầu vào
    source_language = detect(input_text)
    print(f"Detected source language: {source_language}")
    # Xây dựng Prompt dịch thuật
    messages = [
        {"role": "system", "content": "You are a helpful assistant that translates text."},
        {"role": "user", "content": f"Translate the following text from {source_language} to {target_language}: \n{input_text}"}
    ]
    # Gọi API OpenAI để thực hiện dịch thuật
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        max_tokens=512,
        temperature=0.5
    )
    # Lấy kết quả dịch thuật
    translated_text = response.choices[0].message.content.strip()
    print(f"Initial Translation: {translated_text}")
    # Hiệu chỉnh thuật ngữ
    for term, translation in TERMINOLOGY.items():
        translated_text = translated_text.replace(term, translation)
    print(f"Final Translation with Terminology Adjustments: {translated_text}")
    return translated_text
# Kiểm tra dịch đa ngôn ngữ và hiệu chỉnh thuật ngữ
if __name__ == "__main__":
    input_text = "The 5G network uses massive MIMO and beamforming technologies to improve performance."
    translated_output = translate_text(input_text, target_language="fr")
    print("\nFinal Output:\n", translated_output)


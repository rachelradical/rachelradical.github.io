import openai

openai.api_key = "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"  # Replace with your actual key

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Test message"}]
    )
    print("✅ API Key is valid! Response:")
    print(response["choices"][0]["message"]["content"])
except openai.error.AuthenticationError:
    print("❌ API Key is INVALID. Check if you copied it correctly.")
except Exception as e:
    print(f"❌ Error: {e}")

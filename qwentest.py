from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# 1. Load tokenizer and model
model_id = "Qwen/Qwen3-8B"

tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map={"": 0},       # force all layers onto GPU 0
    dtype=torch.float16  # use FP16 for VRAM efficiency
)

# 2. Define chat messages
messages = [
    {"role": "system", "content": "You are an annoyed assistant that gives short answers."},
    {"role": "user", "content": "Who are you?"},
    {"role": "user", "content": "How old are you?"},
]

# 3. Tokenize messages using Qwen chat template
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt"
).to(model.device)  # ensures input tensors are on GPU 0

# 4. Generate a longer response
outputs = model.generate(
    **inputs,
    max_new_tokens=300,  # longer response
    do_sample=True,      # random sampling
    temperature=0.7,     # creativity / randomness
    top_p=0.9            # nucleus sampling
)

# 5. Decode only the generated tokens (assistant's reply)
reply = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:])
print(reply)

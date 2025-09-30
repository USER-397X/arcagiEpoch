from ollama import chat
from ollama import ChatResponse



def main():
    stream = chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
        stream=True,
    )

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)



if __name__ == "__main__":
    main()

# AUTOGENERATED! DO NOT EDIT! File to edit: ../chatGPT_Webapp.ipynb.

# %% auto 0
__all__ = ['api_key', 'generate_response', 'app']

# %% ../chatGPT_Webapp.ipynb 3
import os, openai, fire
import gradio as gr

# %% ../chatGPT_Webapp.ipynb 4
# set openAI API key from your environment varibale $OPENAI_API_KEY
api_key = os.environ.get('OPENAI_API_KEY')
openai.api_key = api_key

def generate_response(model_engine, messages):
    "Deliver the messages to openAI and get a response"
    model_engine = model_engine
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )
    role, content = response['choices'][0]['message']['role'], response['choices'][0]['message']['content']
    messages.append({"role": role, "content": content})
    reply = content
    return reply, messages

def app(IP, Port=5010, model_engine='gpt-3.5-turbo'):
    """
    Launch a local web server of chatGPT
    
    ES:
        --IP your server IP 
        --Port the port you want to use | default=5010
        --model_engine the LLM engine you use from openAI | default='gpt-3.5-turbo'
    """
    chatGPT = gr.Blocks(title='chatGPT by D.X')
    with chatGPT:
        gr.Markdown("<h1><center>ChatGPT of gpt-3.5-turbo</center></h1>")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(placeholder='Input the things you want chatGPT to help you.')
        messages = gr.State(value=[{"role": "system", "content": "You are a helpful assistant."}])
        clear = gr.Button("Clear") 

        def user(user_message, messages, history):
            messages.append({"role": "user", "content": user_message})
            return "", history + [[user_message, None]]

        def bot(user_message, messages, history):
            reply, messages = generate_response(model_engine, messages)
            history[-1][1] = reply
            return history

        msg.submit(user, [msg, messages, chatbot], [msg, chatbot], queue=False).then(
            bot, [msg, messages, chatbot], chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
    
    chatGPT.launch(server_name=IP, server_port=Port, share=True, debug=True)

# %% ../chatGPT_Webapp.ipynb 5
if __name__ == "__main__":
    fire.Fire(app)

from telegram.ext import ApplicationBuilder, CommandHandler
import requests, base64

API_KEY = "sk-Zytg7AMjAn39DzuyNLlK0gqy1JN4Bj0lsN37bFVqQjtuegjb"   

async def imagine(update, context):
    prompt = " ".join(context.args)  # get user input after /imagine
    if not prompt:
        await update.message.reply_text("Please give me a prompt, e.g. /imagine cute anime girl")
        return
    
    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7,
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 25,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        image_base64 = result["artifacts"][0]["base64"]
        with open("output.png", "wb") as f:
            f.write(base64.b64decode(image_base64))
        await update.message.reply_photo(photo=open("output.png", "rb"))
    else:
        await update.message.reply_text("Error: " + response.text)

app = ApplicationBuilder().token("8225064493:AAEyCw-j661DrYOD3ZraosTDYBYaAZ2-pug").build()
app.add_handler(CommandHandler("imagine", imagine))
app.run_polling()

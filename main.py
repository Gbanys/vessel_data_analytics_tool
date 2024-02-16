from pathlib import Path
import uvicorn
import matplotlib.pyplot as plt
from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.extract_vessel_data import extract_relevant_vessel_data
from app.large_language_model import produce_chatbot_response
from nltk.tokenize import word_tokenize
from datetime import datetime
import time
import os

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "vessel_data_analytics_tool" / "app" / "static"),
    name="static",
)

BASE_DIR = Path(__file__).resolve().parent / "app"

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

@app.get("/")
async def return_home_page(request: Request):
    return templates.TemplateResponse(
        "home.html",
        context={
            "request": request,
            "zip": zip
        }
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        user_text = await websocket.receive_text()
        await get_chatbot_response(user_text, websocket)


async def get_chatbot_response(user_text: str, websocket: WebSocket):
    if os.path.exists("app/static/chatbot_plot.png"):
        os.remove("app/static/chatbot_plot.png")
    list_of_words = word_tokenize(user_text, language='english', preserve_line=False)
    vessel_imo = None
    for word in list_of_words:
        if len(word) == 7:
            try:
                vessel_imo = int(word)
            except:
                continue

    time.sleep(1)
    if not vessel_imo:
        await websocket.send_json({'sender' : 'chatbot', 'message': 'Sorry, I do not recognize your vessel imo, please try again.'})
    else:
        vessel_dataframe = extract_relevant_vessel_data(is_unified_data=True, vessel_imo=vessel_imo)
        chatbot_reponse = produce_chatbot_response(vessel_data=vessel_dataframe, query=user_text)
        if 'Axes' in chatbot_reponse.response:
            plt.figure(figsize=(4, 3))
            plot = eval(chatbot_reponse.metadata['pandas_instruction_str'].replace("df", "vessel_dataframe"))
            time_now = datetime.now()
            file_url = f"app/static/chatbot_plot_{time_now}.png".replace(" ", "_").replace(":", "_")
            plot.figure.savefig(file_url)
            time.sleep(2)
            await websocket.send_json({'sender' : 'chatbot_plotter', 'message': file_url.replace("app/", "")})
        else:
            await websocket.send_json({'sender': 'chatbot', 'message': chatbot_reponse.response})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
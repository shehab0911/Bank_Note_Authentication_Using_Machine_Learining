import uvicorn ##ASGI
from fastapi import FastAPI
from BankNotes import BankNote
import pickle
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

pickle_in = open("classifier.pkl","rb")
classifier = pickle.load(pickle_in)

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

@app.get('/')
def index():
    return{'message': 'Hello'}

@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome to fast api': f'{name}'}

@app.post('/predict')
async def predict_note(variance:float =Form(), skewness:float=Form(),curtosis:float=Form(),entropy:float=Form()):

    variance=variance
    skewness=skewness
    curtosis=curtosis
    entropy=entropy

    prediction = classifier.predict([[variance,skewness,curtosis,entropy]])

    if(prediction[0]>0.5):
        Prediction = "Its a fake note"
    else:
        Prediction = "Its a bank note"
    
    return {
        'prediction':Prediction
    }
    #print(Prediction)
    #return templates.TemplateResponse("index.html", {'request': request, 'prediction':Prediction})
    
 

@app.get("/index/", response_class=HTMLResponse)
def read_item(request: Request):
        context = {'request': request}
        return templates.TemplateResponse("index.html", context)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
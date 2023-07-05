from fastapi import FastAPI
from models import Revenue
import pickle
app = FastAPI()
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[30]]))


@app.get("/")
def index():
     return  {"data":"first data"}

@app.post("/predict")
def predict(request:Revenue):
     temp = request.Temperature
     
     predict = model.predict([[temp]])
     return 'The total revenue is ${}'.format(predict)







# if __name__ == "__main__" :
#      uvicorn.run(app)

from fastapi import FastAPI
import uvicorn

def run(args):
    app = FastAPI()

    data = args.get("data", {"msg": "Hello World"})

    @app.get("/")
    def home():
        return data

    print("Starting web server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
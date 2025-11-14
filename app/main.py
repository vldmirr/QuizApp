from fastapi import FastAPI

app = FastAPI()

@app.get("/hi")

def greet():
    return "Hello? World?"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import board, announcement, summarize

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(board.router)
app.include_router(announcement.router)
app.include_router(summarize.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

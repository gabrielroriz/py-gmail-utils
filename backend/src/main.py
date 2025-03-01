
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

from preload import get_mail_base

# Configure logging
logging.basicConfig(level=logging.ERROR)  # Set to ERROR or DEBUG as needed
logger = logging.getLogger(__name__)

origins = ["*"]

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_item(max_results: Optional[int] = None):
    try:
        return get_mail_base(max_results)
    except Exception as e:
        logger.error(f"Error fetching mail base: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
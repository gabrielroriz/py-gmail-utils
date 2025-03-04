
import logging
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

from preload import GmailFetcher, DbFetcher

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

gmail_fetcher = GmailFetcher()
database_fetcher = DbFetcher()

@app.get("/")
async def get_mails(request: Request, 
                    max_results: Optional[int] = None, 
                    from_cloud:Optional[bool] = True, 
                    csv_persist:Optional[bool] = False):
    try:
        return await gmail_fetcher.fetch_emails(request, max_results, from_cloud, csv_persist)
    except Exception as e:
        logger.error(f"Error fetching mail base: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.get("/db")
async def get_databases(request: Request):
    try:
        return await database_fetcher.get_csv_databses(request)
    except Exception as e:
        logger.error(f"Error fetching mail base: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@app.post("/filter")
async def create_filter(request: Request,
                        sender_email: str):
    try:
        return await gmail_fetcher.create_filter(request, sender_email)
    except Exception as e:
        logger.error(f"Error creating filter: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, timeout_keep_alive=7200) #2h timeout
import uvicorn
import sys

if __name__ == "__main__":
  reload = "--reload" in sys.argv
  uvicorn.run("app.app:app", host="0.0.0.0", log_level="info", reload=reload)

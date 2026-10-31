from fastapi import FastAPI, status

from app.routers import courses

app = FastAPI(title="CiteSem API")
app.include_router(courses.router)


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy"}


@app.get("/version", status_code=status.HTTP_200_OK)
def get_version():
    return {"version": "0.1.0", "environment": "development"}
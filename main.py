from fastapi import FastAPI, __version__
from routes import hours, tasks, rol, users
from fastapi.responses import HTMLResponse

app = FastAPI()

html = f"""
<!DOCTYPE html>
<html> 
    <head>
        <title>FastAPI on APPLINKTIC</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

app.include_router(hours.router, prefix="/hours", tags=["hours"])
app.include_router(rol.router, prefix="/rol", tags=["rol"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])
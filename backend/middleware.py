from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5500"],  # change later to your frontend origin
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

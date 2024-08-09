from fastapi import FastAPI, HTTPException, Depends

def register_signal_routes(app: FastAPI):
    @app.get('/signals')
    async def get_signals():
        return {'message': 'Get signals'}
from typing import Annotated
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Depends, Query, WebSocket
from datetime import datetime, timedelta
from .models import SignalRequest 
from app.db import db
from helpers.authorization import get_user_from_token, oauth2_scheme, optional_oauth2_scheme
from .connection_manager import connection_manager

def register_signal_routes(app: FastAPI):


    @app.get('/signals')
    async def get_signals(page: int = Query(1, gt=0), limit: int = Query(10, gt=0)):
        skip = (page - 1) * limit
        query = db['signals'].find().skip(skip).limit(limit)
        signals = []
        for signal in query:
            signal['_id'] = str(signal['_id'])
            signals.append(signal)
        return signals
        
    @app.get('/signals/count')
    async def get_signals_count():
        count = db['signals'].count_documents({})
        return {'count': count }
    
    @app.get('/recent-signals')
    async def get_recent_signals():
        timestamp = datetime.now()
        time_24 = timestamp - timedelta(hours=24)
        query = db['signals'].find({'timestamp': {'$gte': time_24}})
        signals = []
        for signal in query:
            signal['_id'] = str(signal['_id'])
            signals.append(signal)
        return signals
    
    @app.post('/signal')
    async def create_signal(request: SignalRequest, token: Annotated[str, Depends(optional_oauth2_scheme)] = None):
        data = dict(request)
        data["timestamp"] = datetime.now()
        if token:
            data['user'] = get_user_from_token(token)['username']
        print(data)
        db['signals'].insert_one(data)
        return {'message': 'Signal created successfully'}
    
    @app.get('/signal/{signal_id}')
    async def get_signal(signal_id: str):
        signal = db['signals'].find_one({'_id': ObjectId(signal_id)})
        if not signal:
            raise HTTPException(status_code=404, detail='Signal not found')
        signal['_id'] = str(signal['_id'])
        return signal
    
    @app.delete('/signal/{signal_id}')
    async def delete_signal(signal_id: str):
        result = db['signals'].delete_one({'_id': ObjectId(signal_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='Signal not found')
        return {'message': 'Signal deleted successfully'}
    
    @app.websocket('/signal-ws')
    async def websocket_endpoint(websocket: WebSocket):
        await connection_manager.connect(websocket)
        try:
            data = await websocket.receive_text()
            print(data)
        except Exception as e:
            print(e)
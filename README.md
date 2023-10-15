# population counter

API service for population counter. 

To run locally:
1. Define 'MONGO_URL' in '.env' file to point at development database
2. Activate venv (on Windows -> venv\Scripts\activate, on Linux -> source venv/bin/activate)
3. Run command `uvicorn main:app`
4. Open http://127.0.0.1:8000/docs in your browser to see available endpoints

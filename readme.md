Install dependencies:

```
pip install -r requirements.txt
```

Configure the serial port and baud rate in `src/app.py`.

To run the server, run the following command:

```
uvicorn src.app:app --reload --port 8000
```
# adhan-web
Simple Web app for prayer times

![Image of the app](https://github.com/AstroWa3l/adhan-web/blob/main/static/new_pic.png)

## Running the app locally
1. Clone the repository
2. Install the requirements
```bash
pip install -r requirements.txt
```
3. Start backend server
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
4. Start the frontend server in a new terminal window
```bash
npm install
npm run dev
```

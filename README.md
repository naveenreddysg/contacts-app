## create venv
python3 -m venv venv

## move to venv
### Window
.\venv\Scripts\activate.bat

### MAC
source ./venv/bin/activate

## installing requirements
pip install -r requirements.txt

##to run code
python src/app.py

## swagger json to view api documentation
http://localhost:5000/apidocs
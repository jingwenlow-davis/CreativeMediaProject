# CreativeMediaProject

This is the first site I made with the Django framework to get a job at [ASUCD Creative Media](https://creativemedia.ucdavis.edu/).

##### Website is based off of this requirement:
[Front End Template](docs/CM-hiring.png)

### To run locally:
clone repo, create virtual environment and install requirements:
```
git clone https://github.com/jingwenlow/CreativeMediaProject.git
cd CreativeMediaProject
virtualenv -p python3 venv
souce venv/bin/activate
pip install -r requirements.txt
```

run on 127.0.0.1:8000:
```
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```



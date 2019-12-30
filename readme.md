# LolWin Readme
This is a Django Web App for League of Legends analytics

## to download all dependencies for your local environment run
```
python3 -m pip install -r requirements.txt
```

## if you install a package and need to update the requirements use pipreqs
to install pipreqs:
```
pip install pipreqs
```
then run:
```
pipreqs /path/to/project
```
## run migrations
```
python3 manage.py migrate 
```

## to start your local development webserver
```
python3 manage.py runserver
```

## to deploy to gcloud use just push to github master
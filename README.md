# GetAround
Bloc n°5 : Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision

* email : sylvain_mothes@yahoo.fr
* video link : https://share.vidyard.com/watch/gw3sufoSP1ypyDUjnomoKB?


# Dashboard

https://getaround-dasboard-delay-sm.herokuapp.com/

within the directory : dashboard_delay

docker build . -t dashboard
docker run -it -v "$(pwd):/home/app" -p 4000:80 -e PORT=80 dashboard

heroku create getaround-dasboard-delay-sm
heroku container:push web -a getaround-dasboard-delay-sm
heroku container:release web -a getaround-dasboard-delay-sm
heroku open -a getaround-dasboard-delay-sm




# API

https://app-api-getaround.herokuapp.com/docs

within the directory : get_around_pricing

docker build . -t api_getaround
docker run -it -v "$(pwd):/home/app" -p 4000:4000 -e PORT=4000 api_getaround

heroku create app-api-getaround
heroku container:push web -a app-api-getaround
heroku container:release web -a app-api-getaround
heroku open -a app-api-getaround


# GetAround
Bloc n°5 : Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision

* email : sylvain_mothes@yahoo.fr
* video link : https://share.vidyard.com/watch/gw3sufoSP1ypyDUjnomoKB?
* repository's URL : https://github.com/Stylomines/GetAround


# Dashboard

https://getaround-dasboard-delay-sm.herokuapp.com/


within the directory : dashboard_delay

Data : get_around_delay_analysis.xlsx

Deployment :
  - Build docker image and run localy:
      * docker build . -t you_image_dashboard
      * docker run -it -v "$(pwd):/home/app" -p 4000:80 -e PORT=80 you_image_dashboard

  - Create application Heroku:
      * heroku create your_app_dashboard
      * heroku container:push web -a your_app_dashboard
      * heroku container:release web -a your_app_dashboard
      * heroku open -a your_app_dashboard




# API

https://app-api-getaround.herokuapp.com/docs

within the directory : get_around_pricing

Data : get_around_pricing_project.csv
Model ML : model_lr.joblib

Deployment :

  - Build docker image and run localy:
      * docker build . -t your_image_api
      * docker run -it -v "$(pwd):/home/app" -p 4000:4000 -e PORT=4000 your_image_api

  - Create application Heroku:
      * heroku create your_app_api
      * heroku container:push web -a your_app_api
      * heroku container:release web -a your_app_api
      * heroku open -a your_app_api


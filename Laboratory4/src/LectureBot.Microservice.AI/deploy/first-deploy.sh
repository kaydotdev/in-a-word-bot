ssh -T git@github.com
git init
heroku login
heroku git:remote -a lecturesbot-micro-service-ai
git add .
git commit -m "Init commit"
git push heroku master
heroku open


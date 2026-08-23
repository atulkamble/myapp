// Blue Green Deployment 

// app - dev phase 

git clone https://github.com/atulkamble/myapp.git
tree 
python --version
pip --version 
pip install -r requirements.txt
python app.py

// Azure WebApp >> manual 

az webapp deploy -g MyRG -n myapp1234 --src-path app.zip

zip app.zip app.py requirements.txt

// Blue Green Deployment Slot Practice with Azure WebApp Service 

1. create webapp and push code to github repo 
https://github.com/atulkamble/myapp
fork and clone https://github.com/atulkamble/myapp

2. create new branch for same code with different output 
main - production 
green - staging
3. create azure webapp >> select repo >> deployment center >> main - production 
https://myapp1234-g0a7ezc8c8axe7cu.canadacentral-01.azurewebsites.net/

4. create slot >> green (sstaging) 
https://myapp1234-green-hdf9dhcwe6fmctft.canadacentral-01.azurewebsites.net/

5. slot swap >>
https://myapp1234-g0a7ezc8c8axe7cu.canadacentral-01.azurewebsites.net/

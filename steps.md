```text
// Blue Green Deployment - Azure WebApp


// 1. Azure Login

az login

az account show -o table


// 2. Create Resource Group

az group create --name myRG --location canadacentral


// 3. Create App Service Plan

az appservice plan create --name myPythonPlan --resource-group myRG --location canadacentral --sku P0v3 --is-linux


// 4. Check Python Runtime

az webapp list-runtimes --os linux | grep PYTHON


// 5. Create Azure WebApp - Production / Blue

az webapp create --name mypythonapp98600 --resource-group myRG --plan myPythonPlan --runtime "PYTHON:3.14"


// 6. Verify WebApp

az webapp show --name mypythonapp98600 --resource-group myRG -o table


// App - Development Phase

git clone https://github.com/atulkamble/myapp.git

cd myapp

tree

python --version

pip --version

pip install -r requirements.txt

python app.py


// Git - Production Branch

git checkout main

git branch

git add .

git commit -m "production blue version"

git push origin main


// Create ZIP - Production

zip -r blue-app.zip . -x "*.git*"


// Deploy to Production / Blue Slot

az webapp deploy --resource-group myRG --name mypythonapp98600 --src-path blue-app.zip --type zip


// Verify Production

az webapp browse --resource-group myRG --name mypythonapp98600


// -------------------------------------------------------
// Deployment Slot - Green
// -------------------------------------------------------


// Create Green Slot

az webapp deployment slot create --name mypythonapp98600 --resource-group myRG --slot green


// List Slots

az webapp deployment slot list --name mypythonapp98600 --resource-group myRG -o table


// Verify Green Slot

az webapp show --name mypythonapp98600 --resource-group myRG --slot green -o table


// -------------------------------------------------------
// Green Branch
// -------------------------------------------------------


// Create Green Branch

git checkout -b green

git branch


// Change Application Output

// edit app.py
// BLUE VERSION >> GREEN VERSION


// Commit Green Version

git add .

git commit -m "green staging version"

git push -u origin green


// Create ZIP for Green Slot

rm -f green-app.zip

zip -r green-app.zip . -x "*.git*" "blue-app.zip"


// -------------------------------------------------------
// Deploy Application to Green Slot
// -------------------------------------------------------

az webapp deploy --resource-group myRG --name mypythonapp98600 --slot green --src-path green-app.zip --type zip


// Verify Green Slot

az webapp show --resource-group myRG --name mypythonapp98600 --slot green -o table


// Open Green Slot

az webapp browse --resource-group myRG --name mypythonapp98600 --slot green


// -------------------------------------------------------
// Production / Blue Deployment
// -------------------------------------------------------


// Switch to Production Code

git checkout main


// Create Production ZIP

rm -f blue-app.zip

zip -r blue-app.zip . -x "*.git*" "green-app.zip"


// Deploy Main Branch Code to Production

az webapp deploy \
--resource-group myRG \
--name mypythonapp98600 \
--src-path blue-app.zip \
--type zip


// Open Production

az webapp browse \
--resource-group myRG \
--name mypythonapp98600


// -------------------------------------------------------
// Deploy New Version to Green Slot
// -------------------------------------------------------

git checkout green


// Modify app.py

git add .

git commit -m "update green application"

git push origin green


// Re-create Green ZIP

rm -f green-app.zip

zip -r green-app.zip . -x "*.git*" "blue-app.zip"


// Deploy New Version to Green Slot

az webapp deploy \
--resource-group myRG \
--name mypythonapp98600 \
--slot green \
--src-path green-app.zip \
--type zip


// Test Green Slot

az webapp browse \
--resource-group myRG \
--name mypythonapp98600 \
--slot green


// -------------------------------------------------------
// Slot Swap
// -------------------------------------------------------


// Green >> Production

az webapp deployment slot swap \
--resource-group myRG \
--name mypythonapp98600 \
--slot green \
--target-slot production


// Verify Production After Swap

az webapp browse \
--resource-group myRG \
--name mypythonapp98600


// Verify Green Slot After Swap

az webapp browse \
--resource-group myRG \
--name mypythonapp98600 \
--slot green


// -------------------------------------------------------
// Rollback
// -------------------------------------------------------


// Swap Again to Rollback

az webapp deployment slot swap \
--resource-group myRG \
--name mypythonapp98600 \
--slot green \
--target-slot production


// -------------------------------------------------------
// GitHub Deployment Center
// -------------------------------------------------------


// Production / Blue

// Azure Portal
// App Service
// >> Deployment Center
// >> GitHub
// >> Repo: myapp
// >> Branch: main


// Green / Staging

// App Service
// >> Deployment Slots
// >> green
// >> Deployment Center
// >> GitHub
// >> Repo: myapp
// >> Branch: green


// -------------------------------------------------------
// URLs
// -------------------------------------------------------


// Production / Blue

https://myapp1234-g0a7ezc8c8axe7cu.canadacentral-01.azurewebsites.net/


// Green / Staging

https://myapp1234-green-hdf9dhcwe6fmctft.canadacentral-01.azurewebsites.net/


// -------------------------------------------------------
// Flow
// -------------------------------------------------------


// main
// >> Production / Blue
// >> Live Application


// green
// >> Green Slot / Staging
// >> New Version
// >> Test
// >> Swap
// >> Production


// Development Flow

// main >> production

// green >> development changes

// green >> deploy to green slot

// green slot >> test

// green slot >> swap

// green >> production

// issue >> swap again >> rollback
```



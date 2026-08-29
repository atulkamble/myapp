Below is a simple **Azure DevOps YAML pipeline** for your Python Azure Web App Blue-Green setup. It deploys the code to the `green` slot first, then swaps `green` into production. Azure's current `AzureWebApp@1` task supports slot deployment using `deployToSlotOrASE`, `resourceGroupName`, and `slotName`, and `AzureAppServiceManage@0` supports the slot swap. ([Microsoft Learn][1])

```yaml
# azure-pipelines.yml

trigger:
  - main

pool:
  vmImage: 'ubuntu-latest'


variables:

  azureServiceConnection: 'azureconnection'

  resourceGroupName: 'myRG'

  webAppName: 'mypythonapp98600'

  slotName: 'green'

  pythonVersion: '3.14'


stages:


# -------------------------------------------------------
# Stage 1 - Build Python Application
# -------------------------------------------------------

- stage: Build
  displayName: 'Build Python Application'

  jobs:

    - job: BuildApp
      displayName: 'Build Application'

      steps:


        # Checkout Code

        - checkout: self


        # Python Version

        - task: UsePythonVersion@0
          inputs:
            versionSpec: '$(pythonVersion)'
          displayName: 'Use Python $(pythonVersion)'


        # Install Dependencies

        - script: |
            python --version
            pip --version
            pip install -r requirements.txt
          displayName: 'Install Dependencies'


        # Create ZIP Package

        - task: ArchiveFiles@2
          inputs:
            rootFolderOrFile: '$(System.DefaultWorkingDirectory)'
            includeRootFolder: false
            archiveType: 'zip'
            archiveFile: '$(Build.ArtifactStagingDirectory)/app.zip'
            replaceExistingArchive: true
          displayName: 'Create Application ZIP'


        # Publish Artifact

        - task: PublishPipelineArtifact@1
          inputs:
            targetPath: '$(Build.ArtifactStagingDirectory)/app.zip'
            artifact: 'pythonapp'
          displayName: 'Publish Artifact'



# -------------------------------------------------------
# Stage 2 - Deploy to Green Slot
# -------------------------------------------------------

- stage: DeployGreen
  displayName: 'Deploy to Green Slot'

  dependsOn: Build

  jobs:

    - deployment: DeployGreenSlot
      displayName: 'Deploy Green Version'

      environment: 'green'

      strategy:

        runOnce:

          deploy:

            steps:


              # Download Build Artifact

              - task: DownloadPipelineArtifact@2
                inputs:
                  artifact: 'pythonapp'
                  path: '$(Pipeline.Workspace)/pythonapp'
                displayName: 'Download Artifact'


              # Deploy to Green Slot

              - task: AzureWebApp@1
                inputs:
                  azureSubscription: '$(azureServiceConnection)'
                  appType: 'webAppLinux'
                  appName: '$(webAppName)'

                  deployToSlotOrASE: true

                  resourceGroupName: '$(resourceGroupName)'

                  slotName: '$(slotName)'

                  package: '$(Pipeline.Workspace)/pythonapp/app.zip'

                  runtimeStack: 'PYTHON|3.14'

                displayName: 'Deploy to Green Slot'



# -------------------------------------------------------
# Stage 3 - Test Green Slot
# -------------------------------------------------------

- stage: TestGreen
  displayName: 'Test Green Slot'

  dependsOn: DeployGreen

  jobs:

    - job: TestGreenApp
      displayName: 'Test Green Application'

      steps:

        - script: |
            echo "Testing Green Slot"

            curl -f https://$(webAppName)-$(slotName).azurewebsites.net

          displayName: 'Health Check Green Slot'



# -------------------------------------------------------
# Stage 4 - Swap Green to Production
# -------------------------------------------------------

- stage: Swap
  displayName: 'Swap Green to Production'

  dependsOn: TestGreen

  jobs:

    - deployment: SwapSlots
      displayName: 'Swap Deployment Slots'

      environment: 'production'

      strategy:

        runOnce:

          deploy:

            steps:


              - task: AzureAppServiceManage@0

                inputs:

                  azureSubscription: '$(azureServiceConnection)'

                  Action: 'Swap Slots'

                  WebAppName: '$(webAppName)'

                  ResourceGroupName: '$(resourceGroupName)'

                  SourceSlot: '$(slotName)'

                  SwapWithProduction: true

                displayName: 'Swap Green to Production'



# -------------------------------------------------------
# Stage 5 - Verify Production
# -------------------------------------------------------

- stage: VerifyProduction
  displayName: 'Verify Production'

  dependsOn: Swap

  jobs:

    - job: VerifyApp

      steps:

        - script: |

            echo "Testing Production Application"

            curl -f https://$(webAppName).azurewebsites.net

          displayName: 'Test Production'
```

For your setup, replace:

```text
azureconnection
```

with the actual **Azure Resource Manager service connection name** from:

```text
Azure DevOps
>> Project Settings
>> Service Connections
>> Azure Resource Manager
```

The deployment flow is:

```text
main branch
   |
   v
Build Python App
   |
   v
Create app.zip
   |
   v
Deploy to GREEN Slot
   |
   v
Test GREEN
   |
   v
Swap GREEN >> Production
   |
   v
Test Production
```

For a classroom/practice lab, you can also make the swap manually approved by using an Azure DevOps `production` environment with an **Approval and Check**. Then the pipeline stops after green validation and only swaps after approval. ([Microsoft Learn][2])

[1]: https://learn.microsoft.com/th-th/azure/devops/pipelines/tasks/reference/azure-web-app-v1?view=azure-pipelines&utm_source=chatgpt.com "AzureWebApp@1 - Azure Web App v1 task | Microsoft Learn"
[2]: https://learn.microsoft.com/en-us/azure/devops/pipelines/apps/cd/deploy-docker-webapp?view=azure-devops&utm_source=chatgpt.com "Deploy a container to Azure App Service with Azure Pipelines - Azure Pipelines | Microsoft Learn"

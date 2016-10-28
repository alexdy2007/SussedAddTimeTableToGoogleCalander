# SussedAddTimeTableToGoogleCalander
Sorry for crap program structure wrote in anger quickly due to missing a lecture with not been able to view timetable

Adds sussed timetable to your google calander

Need to be run on a linux based system

Pre Reqs
    Python3, Pip3

Build using buildScript in build folder

Create your own google api to access calanders

https://console.developers.google.com
    --> Credentials
      --> Create Credentials
         -->OAuthClientID
            -->Other
              -->Give Name and create

    On DashBoard Near the top Enable API
       --> google calander

    Go Back to DashBoard
       --> far right hand side of your client there is a button Download Json.
           --> Download json file
              --> but it in googleCredentials file under name 'client_secret.json'
              --> if asks server side redirect localhost:8080

In file sussedCredetials.py enter your sussed username and password

to run bin/run.py
if not loading usually due to incorrect driver for chome version. default v52. to change in getClasses file and change to point to correct driver. webdriver.Chrome(dir_path + '/drivers/chromedriverv52')

Can Change number of weeks to get in advance by changing getNumberOfWeekInAdvance in run.py
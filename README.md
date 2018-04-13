# io.maxem.home-assistant

## objective of this project is to create a drive that implements the Maxem.IO api in the home-assistant platform. 

With this driver you are able to switch your Telsa WallConnector on and off in the Home-assistant interface. Todo so you need the following in you configuration.yaml 

switch: 
  - platform: maxem
    email: <<email account with which you login in the Maxem Box>>
    password: <<password>>
    maxemBoxID: <<in the Maxem Box settings (my.maxem.io) you find your Maxem ID>> 

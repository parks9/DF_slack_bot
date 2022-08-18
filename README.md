### Dragonfly Telescope Slack Bot Project

## How to get the code working:

Create a file called ".env" in this same directory and write "SLACK_TOKEN=...", pasting in your own slack token.
You get this token from the slack bot website when you enable socket mode for your app.

You must also have the *dfreduce* package installed from the private dragonfly repo, as well as the slack
package which can be installed directly with pip.

You must also have the standard packages installed (e.g. os, dotenv...) 


## What to do next?

We want to use the S3 Select to get the most recent data from the telescope. Right now, we are using Pandas
DataFrames, so the idea is to save the data from a given night from S3 to an array and then turn it into a 
DataFrame that Pandas can understand. From there, we would run this data through the functions in *summ.py* as usual.

In addition, we have the idea to copy some of the features in *slackbot.py* into the existing night bot's code.
This code is found in the private dragonfly repo.

 

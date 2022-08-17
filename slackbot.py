from DataBase600.upload import data
import pandas as pd
import datetime
import numpy as np
from summ import basic_info, frame_per_lens, flag_count, total_flags
import dfreduce
import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import logging
import os
import time


lightFlags, darkFlags, flatFlags = dfreduce.flags.LightFlags.bit_to_str, dfreduce.flags.DarkFlags.bit_to_str, \
                                    dfreduce.flags.FlatFlags.bit_to_str



def dash_update(data):
    """
    Returns the dashboard info in a formatted message in markdown.
    """
    
    #night = datetime.date.today() - datetime.timedelta(days=1)
    
    test_night = datetime.date(2022,4,7)
    
#     year = int(input("Year of observation:"))
#     month = int(input("Month:"))
#     day = int(input("Day:"))
    
#     night = datetime.date(year, month, day)

    night = test_night
    
    
    is_there = data['date']== str(night)
     
    don = data[is_there]
    
    light, dark, flat, good_l, good_d, good_f = basic_info(don)
    
    flag_names = list(lightFlags.values()), list(darkFlags.values()), list(flatFlags.values())
    
    allflags = total_flags(don, flag_names)
    
    topLightFlag, topDarkFlag, topFlatFlag = lightFlags[np.argmax(allflags[0])], darkFlags[np.argmax(allflags[1])], flatFlags[np.argmax(allflags[2])]
    
    
    if str(night) not in data['date'].values:
        message = '*Data not available for the night of %s.' %(str(night))
    #st.experimental_rerun()
#     st.error('Date not available')
    else:
        message = "*Number of frames*\nThere are %i light frames, %i dark frames and %i flat frames, taken on the night of %s\n\n*Quality of Frames*\n%.1f percent of the light frames had no flags, with %s being the most common flag.\n%.1f percent of the dark frames had no flags, with %s being the most common flag.\n%.1f percent of the flat frames had no flags, with %s being the most common flag." %(light, dark, flat, str(night), good_l, topLightFlag.replace('_', ' '), good_d, topDarkFlag.replace('_', ' '), good_f, topFlatFlag.replace('_', ' '))
    
    return message
   
    
def dash_image(name: str, data):
    # x = np.arange(0, 10, 1)
    # y = np.random.randn(10)
    
    test_night = datetime.date(2022,4,7)
    
#     year = int(input("Year of observation:"))
#     month = int(input("Month:"))
#     day = int(input("Day:"))
    
#     night = datetime.date(year, month, day)

    night = test_night
    
    
    is_there = data['date']== str(night)
     
    don = data[is_there]
    
    LF, DF, FF = list(lightFlags.values()), list(darkFlags.values()), list(flatFlags.values())

    flag_names = list(lightFlags.values()), list(darkFlags.values()), list(flatFlags.values())
    
    all_flags = total_flags(don, flag_names)
    
    
    scale = 25
    width = 0.4
    title_size = 15
    axis_size = 15
    
    
    
    plt.style.use('dark_background')
    
    
    fig = plt.figure()

    x = np.arange(len(LF))

    LF = [i.replace('_', ' ') for i in LF]

    plt.title('Flag Occurences in Light Frames', size=title_size)

    plt.bar(x, all_flags[0], width)
    plt.xlabel('Name of flag', size=axis_size)
    plt.ylabel('Number of each flag', size=axis_size)

    plt.tick_params(axis='y', labelsize=20)
    plt.xticks(x, labels=LF, rotation=65, size=7)

    plt.tight_layout()
    
    plt.savefig(name+"_light.png")
    
    
    
    
    
    fig = plt.figure()

    x2 = np.arange(len(DF))

    DF = [i.replace('_', ' ') for i in DF]

    plt.title('Flag Occurences in Dark Frames', size=title_size)

    plt.bar(x2, all_flags[1], width)
    plt.xlabel('Name of flag', size=axis_size)
    plt.ylabel('Number of each flag', size=axis_size)

    plt.tick_params(axis='y', labelsize=20)
    plt.xticks(x2, labels=DF, rotation=65, size=7)

    plt.tight_layout()
    
    plt.savefig(name+"_dark.png")
    
    
    
    
    
    
    fig = plt.figure()

    x3 = np.arange(len(FF))

    FF = [i.replace('_', ' ') for i in FF]

    plt.title('Flag Occurences in Dark Frames', size=title_size)

    plt.bar(x3, all_flags[2], width)
    plt.xlabel('Name of flag', size=axis_size)
    plt.ylabel('Number of each flag', size=axis_size)

    plt.tick_params(axis='y', labelsize=20)
    plt.xticks(x3, labels=FF, rotation=65, size=7)

    plt.tight_layout()
    
    plt.savefig(name+"_flat.png")
    
    
    
    
    
    time.sleep(6)
    
    return "./"+name+"_light.png", "./"+name+"_dark.png", "./"+name+"_flat.png"
    
    
    
    
    
def multimage(filesdir):
    """
    Send multiple image from a local directory. 
    """
    
    
    logger = logging.getLogger(__name__)

    env_path = Path('.') / '.env'

    load_dotenv(dotenv_path=env_path)

    client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

    # The name of the file you're going to upload
    file_names = [i for i in filesdir]
    
    print(file_names)
    # ID of channel that you want to upload file to
    channel_id = "C03R0H96Q4D"


    # Call the files.upload method using the WebClient
    # Uploading files requires the `files:write` scope
    result1 = client.files_upload(
        channels=channel_id,
        initial_comment="",
        file=file_names[0],
    )
    
    logger.info(result1)
    
    result2 = client.files_upload(
        channels=channel_id,
        initial_comment="",
        file=file_names[1],
    )
    
    
    logger.info(result2)
    
    result3 = client.files_upload(
        channels=channel_id,
        initial_comment="",
        file=file_names[2],
    )
    
    logger.info(result3)
    
    # Log the result
    
    
    
    
    
    
def send_slack_image(filedir: str):
    """
    Send a image from a local file. 
    """
    
    
    logger = logging.getLogger(__name__)

    env_path = Path('.') / '.env'

    load_dotenv(dotenv_path=env_path)

    client = slack.WebClient(token=os.environ["SLACK_TOKEN"])

    # The name of the file you're going to upload
    file_name = filedir
    
    print(file_name)
    # ID of channel that you want to upload file to
    channel_id = "C03R0H96Q4D"


    # Call the files.upload method using the WebClient
    # Uploading files requires the `files:write` scope
    result = client.files_upload(
        channels=channel_id,
        initial_comment="",
        file=file_name,
    )
    # Log the result
    logger.info(result)
    
    
    
def send_slack_message(message: str):
    """
    Send a message to our Slack channel.
    """
    
    import requests
    
    payload = '{"text": "%s"}' % message
    response = requests.post(
    'https://hooks.slack.com/services/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', 
        data = payload
    
    )
    
    print(response.text)

    
    
    
    
    
def main(message_text: str):
    """
    Main function where we can build our logic.
    
    """
    send_slack_message(message = message_text)
    
    
    
    
    
    
    
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Send messages to Slack')
    parser.add_argument('--message', '-m', type=str, default='')
    parser.add_argument('--image', '-i', type=str, default='')
    args = parser.parse_args()
    
    msg = args.message
    image = args.image
    
    if msg == "update":
        main(message_text = dash_update(data))
        
        multimage(dash_image('test', data))
        
    elif len(image) > 0:
        send_slack_image(dash_image(image, data))
    
    
    elif len(msg) > 0:
        main(message_text = msg)
        
    else:
        print('Give me a message.')
        
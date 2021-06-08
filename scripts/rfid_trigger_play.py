#!/usr/bin/env python3

# Reads the card ID or the folder name with audio files
# from the command line (see Usage).
# Then attempts to get the folder name from the card ID
# or play audio folder content directly

# ADD / EDIT RFID CARDS TO CONTROL THE PHONIEBOX
# All controls are assigned to RFID cards in this
# file:
# settings/rfid_trigger_play.conf
# Please consult this file for more information.
# Do NOT edit anything in this file.

import os
import os.path
import sys
import logging
import pathlib
import glob
import argparse
import subprocess
import requests
import xml.etree.ElementTree as ET
import urllib.parse

from pathlib import Path
from datetime import datetime
from shutil import copyfile
from subprocess import Popen, PIPE
from mpd import MPDClient
from functions import *
from PlayoutControl_Class import PlayoutControl

path_current_dir_absolute = str(pathlib.Path(__file__).parent.absolute())
path_dir_root = os.path.abspath(path_current_dir_absolute + "/..")
path_file_debuglog = os.path.abspath(path_dir_root + "/logs/debug.log")


# LOGGING
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(path_file_debuglog),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('rfid_trigger_play')
logger.debug('arguments passed on to script:')

####################################################
# VARIABLES

# ignore files will these extensions in the results:
ignore_file_extension = ('.conf', '.ini', '.jpg', '.db', '.dat', '.*~')

# The absolute path to the folder which contains all the scripts
path_current_dir_absolute=str(pathlib.Path(__file__).parent.absolute())

# config file location
path_dir_root = os.path.abspath(path_current_dir_absolute + "/..")
path_dir_audiofolders = os.path.abspath(path_dir_root + "/shared/audiofolders")
path_dir_settings = os.path.abspath(path_dir_root + "/settings")
path_file_debuglog = os.path.abspath(path_dir_root + "/logs/debug.log")
path_config_global = os.path.abspath(path_dir_settings + "/global.conf")
path_config_debug = os.path.abspath(path_dir_settings + "/debugLogging.conf")
path_config_rfid = os.path.abspath(path_dir_settings + "/rfid_trigger_play.conf")
path_txt_latestID = os.path.abspath(path_dir_root + "/shared/latestID.txt")
path_dir_shortcuts = os.path.abspath(path_dir_root + "/shared/shortcuts")
path_dir_playlists = os.path.abspath(path_dir_root + "/playlists")
# read three config files into one dictionary
conf = read_config_bash([path_config_global, path_config_debug, path_config_rfid])

# Start the future now...: convert some of the old naming into new naming
conf = config_key_conversion(conf)

###################################
# parse variables from command line
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--cardid') # card swiped
parser.add_argument('-d', '--dir') # called with argument directory
parser.add_argument('-v', '--value') # optionally: "recursive" => play also subfolders
args = parser.parse_args()
args_main = vars(args)
logger.debug('arguments passed on to script:')
logger.debug(args_main)

# Set the date and time of now
now_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# create the configuration file from sample - if it does not exist
if Path(path_config_rfid).is_file():
    # file exists
    logger.debug("rfid_trigger_play.conf exists")
else:
    # file does NOT exist
    logger.debug("rfid_trigger_play.conf does NOT exist, copying from settings dir")
    copyfile(path_dir_settings + "/rfid_trigger_play.conf.sample", path_config_rfid)

if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
    logger.debug('configuration found in conf files for global.conf, debugLogging.conf, rfid_trigger_play.conf:')
    logger.debug(conf)

####################################################
# LET THE GAMES BEGIN
playProcess = PlayoutControl(path_dir_root)

#####################################################################
# We might have a card ID, we might not (only folder -d)

if(args_main['cardid']):    
    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
        logger.debug("Card ID given: '%s'" % (args_main['cardid']))

    # Write info to file, making it easer to monitor cards
    with open(path_txt_latestID, "w") as f:
        f.write("Card ID '" + args_main['cardid'] + "' was used at '" + now_string + "'.")
    with open(path_dir_settings + "/Latest_RFID", "w") as f:
        f.write(args_main['cardid'])
    
    # If the input is of 'special' use, don't treat it like a trigger to play audio.
    # Special uses are for example volume changes, skipping, muting sound.
    # NOTE: we need to check if the key exists, because older installations might not have
    # the key in their copied config file. If we don't, the script will throw an error.
    if('CMDSHUFFLE' in conf):
        if(args_main['cardid'] == conf['CMDSHUFFLE']):
            # shuffle currently loaded playlist
            playProcess.playout_playlist_shuffle()
            # subprocess.run("./playout_controls.sh -c=playershuffle", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL30' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL30']):
            # limit volume to 30%
            playProcess.sys_volume_max_set(30)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=30", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL50' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL50']):
            # limit volume to 50%
            playProcess.sys_volume_max_set(50)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=50", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL75' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL75']):
            # limit volume to 75%
            playProcess.sys_volume_max_set(75)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=75", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL80' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL80']):
            # limit volume to 80%
            playProcess.sys_volume_max_set(80)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=80", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL85' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL85']):
            # limit volume to 85%
            subprocess.run("./playout_controls.sh -c=setmaxvolume -v=85", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL90' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL90']):
            # limit volume to 90%
            playProcess.sys_volume_max_set(90)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=90", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL95' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL95']):
            # limit volume to 95%
            playProcess.sys_volume_max_set(95)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=95", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMAXVOL100' in conf):
        if(args_main['cardid'] == conf['CMDMAXVOL100']):
            # limit volume to 100%
            playProcess.sys_volume_max_set(100)
            # subprocess.run("./playout_controls.sh -c=setmaxvolume -v=100", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMUTE' in conf):
        if(args_main['cardid'] == conf['CMDMUTE']):
            # Toggle mute (on / off)
            playProcess.playout_mute_toggle()
            # subprocess.run("./playout_controls.sh -c=mute", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDMUTEFORCE' in conf):
        if(args_main['cardid'] == conf['CMDMUTEFORCE']):
            # Toggle mute (on / off)
            playProcess.playout_mute_force()
            quit() # exit script, because we did what we wanted to do
    if('CMDUNMUTEFORCE' in conf):
        if(args_main['cardid'] == conf['CMDUNMUTEFORCE']):
            # Toggle mute (on / off)
            playProcess.playout_unmute_force()
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL30' in conf):
        if(args_main['cardid'] == conf['CMDVOL30']):
            # set volume to 30%
            playProcess.playout_volume_set(30)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=30", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL50' in conf):
        if(args_main['cardid'] == conf['CMDVOL50']):
            # set volume to 50%
            playProcess.playout_volume_set(50)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=50", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL75' in conf):
        if(args_main['cardid'] == conf['CMDVOL75']):
            # set volume to 75%
            playProcess.playout_volume_set(75)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=75", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL80' in conf):
        if(args_main['cardid'] == conf['CMDVOL80']):
            # set volume to 80%
            playProcess.playout_volume_set(80)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=80", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL85' in conf):
        if(args_main['cardid'] == conf['CMDVOL85']):
            # set volume to 85%
            playProcess.playout_volume_set(85)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=85", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL90' in conf):
        if(args_main['cardid'] == conf['CMDVOL90']):
            # set volume to 90%
            playProcess.playout_volume_set(90)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=90", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL95' in conf):
        if(args_main['cardid'] == conf['CMDVOL95']):
            # set volume to 95%
            playProcess.playout_volume_set(95)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=95", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOL100' in conf):
        if(args_main['cardid'] == conf['CMDVOL100']):
            # set volume to 100%
            playProcess.playout_volume_set(100)
            # subprocess.run("./playout_controls.sh -c=setvolume -v=100", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOLUP' in conf):
        if(args_main['cardid'] == conf['CMDVOLUP']):
            # increase volume by x% set in Audio_Volume_Change_Step
            playProcess.playout_volume_up()
            # subprocess.run("./playout_controls.sh -c=volumeup", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDVOLDOWN' in conf):
        if(args_main['cardid'] == conf['CMDVOLDOWN']):
            # decrease volume by x% set in Audio_Volume_Change_Step
            playProcess.playout_volume_down()
            # subprocess.run("./playout_controls.sh -c=volumedown", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDSTOP' in conf):
        if(args_main['cardid'] == conf['CMDSTOP']):
            # kill all running audio players
            playProcess.playout_stop()
            # subprocess.run("./playout_controls.sh -c=playerstop", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDNEXT' in conf):
        if(args_main['cardid'] == conf['CMDNEXT']):
            # play next track in playlist 
            playProcess.playout_next()
            # subprocess.run("./playout_controls.sh -c=playernext", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDPREV' in conf):
        if(args_main['cardid'] == conf['CMDPREV']):
            # play previous track in playlist 
            playProcess.playout_prev()
            # subprocess.run("./playout_controls.sh -c=playerprev", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDREWIND' in conf):
        if(args_main['cardid'] == conf['CMDREWIND']):
            # start with first track in playlist 
            playProcess.playout_restart()
            # subprocess.run("./playout_controls.sh -c=playerrewind", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDSEEKFORW' in conf):
        if(args_main['cardid'] == conf['CMDSEEKFORW']):
            # jump 15 seconds ahead 
            subprocess.run("./playout_controls.sh -c=playerseek -v=+15", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDSEEKBACK' in conf):
        if(args_main['cardid'] == conf['CMDSEEKBACK']):
            # jump 15 seconds back 
            subprocess.run("./playout_controls.sh -c=playerseek -v=-15", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDPAUSE' in conf):
        if(args_main['cardid'] == conf['CMDPAUSE']):
            # toggle pause of current playback 
            playProcess.playout_pause_toggle()
            # subprocess.run("./playout_controls.sh -c=playerpause", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDPAUSEFORCE' in conf):
        if(args_main['cardid'] == conf['CMDPAUSEFORCE']):
            # force pause current track 
            playProcess.playout_pause_force()
            quit() # exit script, because we did what we wanted to do
    if('CMDPLAY' in conf):
        if(args_main['cardid'] == conf['CMDPLAY']):
            # play / resume current track  
            playProcess.playout_play_force()
            # subprocess.run("./playout_controls.sh -c=playerplay", shell=False)
            quit() # exit script, because we did what we wanted to do

    #################################            
    # SYSTEM COMMANDS AFTER THIS LINE
    # system_controls.sh
    
    if('CMDRANDCARD' in conf):
        if(args_main['cardid'] == conf['CMDRANDCARD']):
            # activate a random card 
            subprocess.run("./system_controls.sh -c=randomcard", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDRANDFOLD' in conf):
        if(args_main['cardid'] == conf['CMDRANDFOLD']):
            # play a random folder 
            subprocess.run("./system_controls.sh -c=randomfolder", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDRANDTRACK' in conf):
        if(args_main['cardid'] == conf['CMDRANDTRACK']):
            # jump to a random track in playlist (no shuffle mode required) 
            subprocess.run("./system_controls.sh -c=randomtrack", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('STOPAFTER5' in conf):
        if(args_main['cardid'] == conf['STOPAFTER5']):
            # stop player after -v minutes 
            subprocess.run("./system_controls.sh -c=playerstopafter -v=5", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('STOPAFTER15' in conf):
        if(args_main['cardid'] == conf['STOPAFTER15']):
            # stop player after -v minutes 
            subprocess.run("./system_controls.sh -c=playerstopafter -v=15", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('STOPAFTER30' in conf):
        if(args_main['cardid'] == conf['STOPAFTER30']):
            # stop player after -v minutes 
            subprocess.run("./system_controls.sh -c=playerstopafter -v=30", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('STOPAFTER60' in conf):
        if(args_main['cardid'] == conf['STOPAFTER60']):
            # stop player after -v minutes 
            subprocess.run("./system_controls.sh -c=playerstopafter -v=60", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNAFTER5' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNAFTER5']):
            # shutdown RPi after -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownafter -v=5", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNAFTER15' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNAFTER15']):
            # shutdown RPi after -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownafter -v=15", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNAFTER30' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNAFTER30']):
            # shutdown RPi after -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownafter -v=30", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNAFTER60' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNAFTER60']):
            # shutdown RPi after -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownafter -v=60", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNVOLUMEREDUCTION10' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNVOLUMEREDUCTION10']):
            # reduce volume until shutdown in -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownvolumereduction -v=10", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNVOLUMEREDUCTION15' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNVOLUMEREDUCTION15']):
            # reduce volume until shutdown in -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownvolumereduction -v=15", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNVOLUMEREDUCTION30' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNVOLUMEREDUCTION30']):
            # reduce volume until shutdown in -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownvolumereduction -v=30", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('SHUTDOWNVOLUMEREDUCTION60' in conf):
        if(args_main['cardid'] == conf['SHUTDOWNVOLUMEREDUCTION60']):
            # reduce volume until shutdown in -v minutes 
            subprocess.run("./system_controls.sh -c=shutdownvolumereduction -v=60", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('ENABLEWIFI' in conf):
        if(args_main['cardid'] == conf['ENABLEWIFI']):
            subprocess.run("./system_controls.sh -c=enablewifi", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('DISABLEWIFI' in conf):
        if(args_main['cardid'] == conf['DISABLEWIFI']):
            subprocess.run("./system_controls.sh -c=disablewifi", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('TOGGLEWIFI' in conf):
        if(args_main['cardid'] == conf['TOGGLEWIFI']):
            subprocess.run("./system_controls.sh -c=togglewifi", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDPLAYCUSTOMPLS' in conf):
        if(args_main['cardid'] == conf['CMDPLAYCUSTOMPLS']):
            subprocess.run("./system_controls.sh -c=playlistaddplay -v=PhonieCustomPLS -d=PhonieCustomPLS", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('RECORDSTART600' in conf):
        if(args_main['cardid'] == conf['RECORDSTART600']):
            # start recorder for -v seconds 
            subprocess.run("./system_controls.sh -c=recordstart -v=600", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('RECORDSTART60' in conf):
        if(args_main['cardid'] == conf['RECORDSTART60']):
            # start recorder for -v seconds 
            subprocess.run("./system_controls.sh -c=recordstart -v=60", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('RECORDSTART10' in conf):
        if(args_main['cardid'] == conf['RECORDSTART10']):
            # start recorder for -v seconds 
            subprocess.run("./system_controls.sh -c=recordstart -v=10", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('RECORDSTOP' in conf):
        if(args_main['cardid'] == conf['RECORDSTOP']):
            # start recorder for -v seconds 
            subprocess.run("./system_controls.sh -c=recordstop", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('RECORDPLAYBACKLATEST' in conf):
        if(args_main['cardid'] == conf['RECORDPLAYBACKLATEST']):
            # play the latest recording 
            subprocess.run("./system_controls.sh -c=recordplaylatest", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDREADWIFIIP' in conf):
        if(args_main['cardid'] == conf['CMDREADWIFIIP']):
            # read the current WiFi IP address over the speaker 
            subprocess.run("./system_controls.sh -c=readwifiipoverspeaker", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDBLUETOOTHTOGGLE' in conf):
        if(args_main['cardid'] == conf['CMDBLUETOOTHTOGGLE']):
            subprocess.run("./system_controls.sh -c=bluetoothtoggle -v=toggle", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDSWITCHAUDIOIFACE' in conf):
        if(args_main['cardid'] == conf['CMDSWITCHAUDIOIFACE']):
            # switch between primary/secondary audio iFaces
            subprocess.run("./system_controls.sh -c=switchaudioiface", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDSHUTDOWN' in conf):
        if(args_main['cardid'] == conf['CMDSHUTDOWN']):
            # shutdown the RPi nicely
            subprocess.run("./system_controls.sh -c=shutdown", shell=False)
            quit() # exit script, because we did what we wanted to do
    if('CMDREBOOT' in conf):
        if(args_main['cardid'] == conf['CMDREBOOT']):
            # reboot the RPi 
            subprocess.run("./system_controls.sh -c=reboot", shell=False)
            quit() # exit script, because we did what we wanted to do
    
    ################################################################
    # We checked if the card was a special command, seems it wasn't.
    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
        log_message = "Card ID is not linked to a system command"
        logger.info(log_message)
    
    # Now we expect it to be a trigger for one or more audio file(s).
    # Let's look at the ID, write a bit of log information and then try to play audio.
    
    # Look for human readable shortcut in folder 'shortcuts'
    path_shortcut_id = path_dir_shortcuts + "/" + args_main['cardid']
    
    # check if CARDID has a text file by the same name - which would contain the human readable folder name    
    if Path(path_shortcut_id).is_file():
        # file exists
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug("CARDID does exist as file in shortcuts folder")
        # Read human readable shortcut from file
        folder_name = Path(path_shortcut_id).read_text().strip()
        # Add info into the log, making it easer to monitor cards
        with open(path_txt_latestID, "a") as f:
            f.write("\nThis ID has been used before.")
    else:
        # file does NOT exist
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug("CARDID does NOT exist as file in shortcuts folder")
        # Human readable shortcut does not exist, so create one with the content $CARDID
        # this file can later be edited manually over the samba network
        with open(path_shortcut_id, "w") as f:
            f.write(args_main['cardid'])
        # Add info into the log, making it easer to monitor cards
        with open(path_txt_latestID, "a") as f:
            f.write("\nThis ID was used for the first time.")
        # Create human readable shortcut from card id
        folder_name = args_main['cardid']
    
    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
        logger.debug("Folder name found: " + folder_name)

else:
    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
        logger.debug('Card ID not given, check if directory given')
    if('dir' in args_main):
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug("Directory given: '%s'" % (args_main['dir']))
        folder_name = args_main['dir']
    else:
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug('And no directory given, there is nothing to do...')
            


##############################################################
# We should now have a folder name with the audio files.
# Either from prompt of from the card ID processing above

# check if
# - folder_name is not empty: if folder_name
# - folder_name exists: os.path.exists(path_folder_name)
# - folder_name is a directory: os.path.isdir(path_folder_name)

path_folder_name = conf['AUDIO_FOLDER_PATH'] + "/" + folder_name.strip() + "/"

if folder_name and os.path.exists(path_folder_name) and os.path.isdir(path_folder_name):
    if not os.listdir(path_folder_name):
        # Directory is empty
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug(path_folder_name + " does not exist - if not os.listdir(path_folder_name)")
    else:    
        # Directory is not empty -> PLAY THE FOLDER CONTENT
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug(path_folder_name + " is not empty")

        # if we play a folder the first time, add some sensible information to the folder.conf file
        if os.path.exists(path_folder_name + "folder.conf"):
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("folder.conf file exists")
        else:
            # now we create a default folder.conf file by calling inc.writeFolderConfig.sh
            # with the command param createDefaultFolderConf
            # see inc.writeFolderConfig.sh for details
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("folder.conf does not exist, create one")
            subprocess.run("./inc.writeFolderConfig.sh -c=createDefaultFolderConf -d='" + folder_name + "'", shell=False)

        # get the name of the last folder and playlist played. 
        # As mpd doesn't store the name of the last playlist, 
        # we have to keep track of it via the Latest_Folder_Played / Latest_Playlist_Played file
        folder_last_played_name = Path(path_dir_settings + "/Latest_Folder_Played").read_text().strip()
        playlist_last_played_name = Path(path_dir_settings + "/Latest_Playlist_Played").read_text().strip()
        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.info("folder_last_played_name: " + folder_last_played_name)
            logger.info("playlist_last_played_name: " + playlist_last_played_name)
        
        #####################
        # CREATE THE PLAYLIST
        
        # replace subfolder slashes with " % "
        playlist_name = folder_name.replace("/", " % ")

        # default search for files => the directory (only)
        dirs_audio = [path_folder_name]

        # recursive search (folder and subfolders)?
        if('value' in args_main):
            if(args_main['value'] == "recursive"):
                # the folder_name directory and subdirectories
                dirs_audio = [] # directories
                # read folders recursively into list dirs_audio
                for dirpath, dirs, files in os.walk(path_folder_name):
                	dirs_audio += [dirpath]
                # replace subfolder slashes with " % "
                playlist_name = playlist_name + "-%RCRSV%"

        if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
            logger.debug("Folders to check for audio (dirs_audio):")
            logger.debug(dirs_audio)

        # go through folders
        playlist_files = [] # final playlist
        for dir_audio in dirs_audio:
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("Collecting audio in folder: '%s'" % (dir_audio))
            playlist_files_temp = [] # temporary playlist for each folder
            if Path(dir_audio + '/livestream.txt').is_file():
                #######################
                # check for livestreams
                file_check = dir_audio + '/livestream.txt'
                # add content of file to playlist
                file_content = open(file_check,'r').read().strip()
                playlist_files_temp = [file_content]
                # merge files into master playlist
                playlist_files += playlist_files_temp
            elif Path(dir_audio + '/podcast.txt').is_file():
                ###################
                # check for podcast
                file_check = dir_audio + '/podcast.txt'
                # add content of file to playlist
                # read URL content as text to var rss
                file_content = open(file_check,'r').read().strip()
                rss = requests.get(file_content).text
                # parse rss XML to find enclosure tags
                tree = ET.fromstring(rss)
                enclosures = tree.findall(".//enclosure") # Use the XPath to find all enclosure elements 
                for enclosure in  enclosures:
                    #url = enclosure.attrib['url'].split('?')[0] # cuts off the tail, but might not work for all URLs
                    #url = enclosure.attrib['url'] # complete URL
                    playlist_files_temp += [enclosure.attrib['url']]
                # merge files into master playlist
                playlist_files += playlist_files_temp
            elif Path(dir_audio + '/spotify.txt').is_file():
                ############################
                # check for spotify playlist
                file_check = dir_audio + '/spotify.txt'
                # add content of file to playlist
                file_content = open(file_check,'r').read().strip()
                playlist_files_temp = [file_content]
                # merge files into master playlist
                playlist_files += playlist_files_temp
            else:
                ##########################
                # normal files (finally :)
                playlist_files_all = glob.glob(dir_audio + '/*.*')
                # filter file extensions, see tuple with filter at the beginning of this file
                # NOTE: glob has exclusion options, research if this could be done above.
                # example excludes all files ending with a 't': 
                # playlist_files = glob.glob(path_name_audio + '/**/*.[!t]*', recursive=True)
                playlist_files_temp = [file for file in playlist_files_all if not file.endswith(ignore_file_extension)]
                # merge files into master playlist
                playlist_files_temp.sort()
                playlist_files += playlist_files_temp
        
        # now we need to make sure the local files work for Mopidy
        if conf['EDITION'].strip('"') == "plusSpotify":
            playlist_files = [urllib.parse.quote(file.replace(myvars['AUDIOFOLDERSPATH'].strip('"') + "/", 'local:track:')) for file in playlist_files]
            playlist_files = [file.replace('local%3Atrack%3A', 'local:track:') for file in playlist_files]

        # write file to playlists folder
        with open(path_dir_playlists + "/" + playlist_name + ".m3u", mode='wt', encoding='utf-8') as myfile:
            myfile.write('\n'.join(playlist_files))
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("Written playlist to file: '%s':" % (path_dir_playlists + "/" + playlist_name + ".m3u"))
                logger.debug(playlist_files)
                
        ############################################
        # SAVE PLAYLIST POSITION OF CURRENT PLAYLIST
        # ??? this does not work yet... ???
        playProcess.playout_position_save()

        ##############
        # SECOND SWIPE

        # Available 
        # * RESTART => Re-start playlist 
        # * SKIPNEXT => Skip to next track 
        # * PAUSE => Toggle pause / play 
        # * PLAY => Resume playback 
        # * NOAUDIOPLAY => Ignore audio playout triggers, only system commands

        # Setting a VAR to start "play playlist from start"
        # This will be changed in the following checks "if this is the second swipe"
        playlist_play = "default"
        
        ####################################
        # Check if the second swipe happened
        
        if(playlist_name == playlist_last_played_name):
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.info("SECOND SWIPE: Current playlist has been swiped twice")
            
            # Connect with mpd
            client = MPDClient()               # create client object
            client.timeout = 10                # network timeout in seconds (floats allowed), default: None
            client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
            client.connect("localhost", 6600)  # connect to localhost:6600
            mpd_status = client.status()
            # mpd_status playing example:     {'volume': '67', 'repeat': '0', 'random': '0', 'single': '0', 'consume': '0', 'playlist': '32', 'playlistlength': '3', 'mixrampdb': '0.000000', 'state': 'play', 'song': '2', 'songid': '88', 'time': '1:2', 'elapsed': '0.754', 'bitrate': '128', 'duration': '2.324', 'audio': '44100:24:2'}
            # mpd_status not playing example: {'volume': '67', 'repeat': '0', 'random': '0', 'single': '0', 'consume': '0', 'playlist': '34', 'playlistlength': '3', 'mixrampdb': '0.000000', 'state': 'stop'}
            logger.debug("mpd_status:")
            logger.debug(mpd_status)
            # close and disconnect from mpd
            client.close()  # send the close command
            client.disconnect()
    
            if(conf['SECONDSWIPE'] == "RESTART"):
                if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                    logger.debug("RESTART => Re-start playlist")
                # PLAY playlist from beginning
                playProcess.playout_restart()
                playlist_play = "ignore" # don't play playlist below
        
            elif(conf['SECONDSWIPE'] == "SKIPNEXT"):
                if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                    logger.debug("SKIPNEXT => Skip to next track")
                # End of playlist? if no 'song' is given in 'mpd_status'
                if('song' not in mpd_status):
                    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                       logger.debug("Playlist ended, so start from top")
                    # Assuming the playlist ended, second swipe will restart (not skip)
                else:
                    # We will not play the playlist but skip to the next track
                    playlist_play = "ignore" # don't play playlist below
                    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                        logger.debug("mpd playing, so skip")
                    playProcess.playout_next()
                    playlist_play = "ignore" # don't play playlist below
        
            elif(conf['SECONDSWIPE'] == "PAUSE"):
                if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                    logger.debug("PAUSE => Toggle pause / play")
                # if playlist_length == 0 do always play, bc first swipe after reboot
                if mpd_status['playlistlength'] == 0:
                    logger.debug("no playlist")
                else:
                    playlist_play = "ignore" # don't play playlist below
                    # play / pause toggle
                    playProcess.playout_pause_toggle()
        
            elif(conf['SECONDSWIPE'] == "PLAY"):
                if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                    logger.debug("PLAY => Resume playback")
                # same as normal playout PLUS: forcing *resume*
                args_func = {}
                args_func['dirpath'] = folder_name
                args_func['playlistname'] = playlist_name
                args_func['value'] = "RESUME"

                playProcess.playout_resume_play(args_func)
                playlist_play = "ignore" # don't play playlist below
        
            elif(conf['SECONDSWIPE'] == "NOAUDIOPLAY"):
                if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                    logger.debug("NOAUDIOPLAY => Ignore audio playout triggers, only system commands")
                # End of playlist? if no 'song' is given in 'mpd_status'
                if('song' not in mpd_status):
                    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                        logger.debug("Playlist will be played, because playlist ended")
                    # do nothing, because the playlist will be played from top at the end of this file
                    # because still: playlist_play = "default"
                else:
                    playlist_play = "ignore" # don't play playlist below
        else:
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("Current playlist has not been swiped twice")
        
        # end of second swipe check
        ###########################
        
        # now see if we need to play the playlist or if it has been played already as part of second swipe?
        if(playlist_play == "default"):
            if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
                logger.debug("Play playlist from top:" + playlist_name)

            # Save the name of the playlist before we leave
            with open(path_dir_settings + "/Latest_Playlist_Played", "w") as f:
                f.write(playlist_name)
            os.chmod(path_dir_settings + "/Latest_Playlist_Played", 0o0777)

            # PLAY playlist
            args_func = {}
            args_func['dirpath'] = folder_name
            args_func['playlistname'] = playlist_name
            playProcess.playout_playlist_load_play(args_func)
            logger.debug("Executed: playProcess.playout_playlist_load_play")

else:
    # Given directory doesn't exist
    if conf['DEBUG_rfid_trigger_play_sh'] == "TRUE":
        logger.debug(path_folder_name + " does not exist")

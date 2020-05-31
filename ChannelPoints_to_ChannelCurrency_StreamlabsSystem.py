# -*- coding: utf-8 -*-

# Importing Required Libraries
import clr, codecs, json, os, re, sys, threading, datetime

clr.AddReference("IronPython.Modules.dll")
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)) + "\References", "TwitchLib.PubSub.dll"))
from TwitchLib.PubSub import TwitchPubSub


#   Required Script Information
ScriptName = "Twitch Channel Points to Currency"
Website = "https://www.twitch.tv/IceyGlaceon"
Description = "Script to trigger automagically add currency for users that use channel point reward redemptions."
Creator = "IceyGlaceon"
Version = "1.0.0"

#  Required Define Global Variables
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")
README = os.path.join(os.path.dirname(__file__), "README.md")
EventReceiver = None
ThreadQueue = []
CurrentThread = None
PlayNextAt = datetime.datetime.now()

class Settings(object):
    def __init__(self, SettingsFile=None):
        if SettingsFile and os.path.isfile(SettingsFile):
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        else:
            self.EnableDebug = True
            self.TwitchOAuthToken = ""
            self.TwitchReward1Name = ""
            self.R1Points = 1000
            self.TwitchReward2Name = ""
            self.R2Points = 1000
            self.TwitchReward3Name = ""
            self.R3Points = 1000
            self.TwitchReward4Name = ""
            self.R4Points = 1000


    def Reload(self, jsondata):
        self.__dict__ = json.loads(jsondata, encoding="utf-8")
        return

    def Save(self, SettingsFile):
        try:
            with codecs.open(SettingsFile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
            with codecs.open(SettingsFile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8')))
        except:
            Parent.Log(ScriptName, "Failed to save settings to the file. Fix error and try again.")
        return

#   [Required] Initialize Data (Only called on load)
def Init():
    global ScriptSettings
    ScriptSettings = Settings(SettingsFile)
    ScriptSettings.Save(SettingsFile)

    ## Init the Streamlabs Event Receiver
    Start()

    return

def Start():
    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Starting receiver");

    global EventReceiver
    EventReceiver = TwitchPubSub()
    EventReceiver.OnPubSubServiceConnected += EventReceiverConnected
    EventReceiver.OnRewardRedeemed += EventReceiverRewardRedeemed

    EventReceiver.Connect()

def EventReceiverConnected(sender, e):

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Event receiver connecting")
# -----------------------------------
#  Get Channel ID for Username
# -----------------------------------
    headers = {
        "Client-ID": "icyqwwpy744ugu5x4ymyt6jqrnpxso",
        "Authorization": "Bearer " + ScriptSettings.TwitchOAuthToken[6:]
    }
    result = json.loads(Parent.GetRequest("https://api.twitch.tv/helix/users?login=" + Parent.GetChannelName(), headers))
    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "result: " + str(result))
    user = json.loads(result["response"])
    id = user["data"][0]["id"]

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Event receiver connected, sending topics for channel id: " + id)

    EventReceiver.ListenToRewards(id)
    EventReceiver.SendTopics(ScriptSettings.TwitchOAuthToken)
    return

# -----------------------------------
#  Actual Conversion and Application Done Here
# -----------------------------------
def EventReceiverRewardRedeemed(sender, e):
    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Event triggered")
        # e.DisplayName == streamlabs chatbot data.UserName. e.Login == streamlabs chatbot data.User
        # This does NOT transfer equally for youtube/mixer. Use resources in README for alternatives.
        Parent.Log(ScriptName, "Testing twitch reward name: " + e.RewardTitle)
        Parent.Log(ScriptName, "This is the TwitchReward1Name: " + ScriptSettings.TwitchReward1Name)
        dataUser = e.Login
        dataUserName = e.DisplayName
        reward = e.RewardTitle
    if e.RewardTitle == ScriptSettings.TwitchReward1Name:
        ThreadQueue.append(threading.Thread(target=RewardRedeemedWorker,args=(reward, ScriptSettings.R1Points, dataUser, dataUserName)))
    if e.RewardTitle == ScriptSettings.TwitchReward2Name:
        ThreadQueue.append(threading.Thread(target=RewardRedeemedWorker,args=(reward, ScriptSettings.R2Points, dataUser, dataUserName)))
    if e.RewardTitle == ScriptSettings.TwitchReward3Name:
        ThreadQueue.append(threading.Thread(target=RewardRedeemedWorker,args=(reward, ScriptSettings.R3Points, dataUser, dataUserName)))
    if e.RewardTitle == ScriptSettings.TwitchReward4Name:
        ThreadQueue.append(threading.Thread(target=RewardRedeemedWorker,args=(reward, ScriptSettings.R4Points, dataUser, dataUserName)))
    return

def RewardRedeemedWorker(reward, amount, dataUser, dataUserName):
    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, dataUserName + " is redeeming " + reward + " for " + str(amount) + " units worth of channel currency")

    Parent.AddPoints(dataUser,dataUserName,long(str(amount)))

    global PlayNextAt
    PlayNextAt = datetime.datetime.now() + datetime.timedelta(0, delay)


#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
def Execute(data):
    return

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():

    global PlayNextAt
    if PlayNextAt > datetime.datetime.now():
        return

    global CurrentThread
    if CurrentThread and CurrentThread.isAlive() == False:
        CurrentThread = None

    if CurrentThread == None and len(ThreadQueue) > 0:
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, "Starting new thread. " + str(PlayNextAt))
        CurrentThread = ThreadQueue.pop(0)
        CurrentThread.start()

    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters)
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString
#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here

    if ScriptSettings.EnableDebug:
        Parent.Log(ScriptName, "Saving settings.")

    global EventReceiver
    try:
        if EventReceiver:
            EventReceiver.Disconnect()

        ScriptSettings.__dict__ = json.loads(jsonData)
        ScriptSettings.Save(SettingsFile)
        EventReceiver = None

        Start()
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, "Settings saved successfully")
    except Exception as e:
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, str(e))

    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    # Disconnect EventReceiver cleanly
    try:
        if EventReceiver:
            EventReceiver.Disconnect()
    except:
        if ScriptSettings.EnableDebug:
            Parent.Log(ScriptName, "Event receiver already disconnected")

    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it). Do not rename openreadme.
#---------------------------
def ScriptToggled(state):
    return

def openreadme():
    os.startfile(README)

def GetToken():
	os.startfile("https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=icyqwwpy744ugu5x4ymyt6jqrnpxso&redirect_uri=https://twitchapps.com/tmi/&scope=channel:read:redemptions&force_verify=true")

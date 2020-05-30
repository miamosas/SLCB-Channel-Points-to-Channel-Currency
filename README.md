# SLCB Channel Points to Channel Currency Script

This script allows users to use exchange their earned channel points for your personal channel currency!
This bot does not have a cool down and should work even if someone redeems in rapid succession.

## Installing

This script was built for use with Streamlabs Chatbot.
Follow instructions on how to install custom script packs at:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts

Click [Here](https://github.com/Encrypted-Thoughts/SLCB-ChannelPointsSFXTrigger/blob/master/ChannelPointsSFXTrigger.zip?raw=true) to download the script pack directly.

Once installed you will need to provide an oAuth token. You can get one by clicking the Get Token button in script settings.
This button also exists in the streamlabs chatbot UI. Make sure you don't show this token on stream, it is as sensitive
as your stream key!

![token](https://user-images.githubusercontent.com/50642352/82402817-f8165480-9a22-11ea-8810-fc93899d785a.png)

## Use

Once installed, just add custom channel point rewards to your twitch channel and then _exactly_ match the names of the reward to a Twitch Reward event in the script settings within Streamlabs OBS. In this example, please refer to `Point Testing` that costs `25 Channel Points`

![image1](https://user-images.githubusercontent.com/64919861/83341215-9c0ac600-a295-11ea-997b-2fc5a16df307.png)

![image2](https://user-images.githubusercontent.com/64919861/83341207-7978ad00-a295-11ea-9094-76d697e2395a.png)

## Author

IceyGlaceon - [Twitch](https://www.twitch.tv/iceyglaceon), [Twitter](https://www.twitter.com/theiceyglaceon)


## References

This script makes use of TwitchLib's pubsub listener to detect the channel point redemptions. Go check out their repo at https://github.com/TwitchLib/TwitchLib for more info.

This script is based off of [EncryptedThoughts's Channel Point's SFX Trigger.](https://github.com/Encrypted-Thoughts/SLCB-ChannelPointsSFXTrigger)
Check out their [Twitch](https://www.twitch.tv/EncryptedThoughts)!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

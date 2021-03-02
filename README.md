# SLCB Channel Points to Channel Currency Script

This script allows users to use exchange their earned channel points for your personal channel currency!
This bot does not have a cool down and should work even if someone redeems in rapid succession.

## Installing

This script was built for use with Streamlabs Chatbot.
Follow instructions on how to install custom script packs at:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts

Click [Here](https://github.com/iceyglaceon/SLCB-Channel-Points-to-Channel-Currency/blob/master/ChannelPointsToChannelCurrency.zip?raw=true) to the script pack directly.

Once installed you will need to provide an oAuth token. You can get one by clicking the Get Token button in script settings.
This button also exists in the streamlabs chatbot UI. Make sure you don't show this token on stream, it is as sensitive
as your stream key!

![token](https://user-images.githubusercontent.com/50642352/82402817-f8165480-9a22-11ea-8810-fc93899d785a.png)

## Use

Once installed, just add custom channel point rewards to your twitch channel and then _exactly_ match the names of the reward to a Twitch Reward event in the script settings within Streamlabs OBS. In this example, please refer to `Point Testing` that costs `25 Channel Points`

![image1](https://user-images.githubusercontent.com/64919861/83341215-9c0ac600-a295-11ea-997b-2fc5a16df307.png)

![image2](https://user-images.githubusercontent.com/64919861/83341207-7978ad00-a295-11ea-9094-76d697e2395a.png)

## Logging
I highly recommend turning on debugging/logging before you rock and roll with this script. A script that shows this is working properly looks like this: 

![image3](https://user-images.githubusercontent.com/64919861/83362483-7c7fa600-a346-11ea-8345-e46cd7fd804a.png)

## Author

Miamosas - [Twitch](https://www.twitch.tv/miamosas), [Twitter](https://www.twitter.com/miamosas)

## Changelog
v. 1.0.0 - Initial Commit
v. 1.0.1 - Fixed a bug where only tier 1 currency amount was getting added. Fixed an error where variables were only happening if debugging was on. Bumped version. 
## References

This script makes use of TwitchLib's pubsub listener to detect the channel point redemptions. Go check out their repo at https://github.com/TwitchLib/TwitchLib for more info.

This script is based off of [EncryptedThoughts's Channel Point's SFX Trigger.](https://github.com/Encrypted-Thoughts/SLCB-ChannelPointsSFXTrigger)
Check out their [Twitch](https://www.twitch.tv/EncryptedThoughts)!

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

# YoutubeLive API
this repo uses [YoutubeDataAPI](https://developers.google.com/youtube/v3/live/docs/liveChatMessages) to get live chats.
## Response data format
```json
{
    "user"       : string,
    "msg"        : string,
    "isSuper"    : bool,
    "superAmount": string,
    "superMsg"   : string,
    "isOwner"    : bool
}
```

## Properties
| key | type | description | YoutubeDataAPI |
|---|---|---|---|
|user|string|user name who chatted.|authorDetails.displayName|
|msg|string|chat message.|snippet.displayMessage|
|isSuper|bool|This value indicates whether the chat is super chat.|
|superAmount|string|purchase amount and currency, like $1.00.|snippet.superChatDetails.amountDisplayString|
|superMsg|string|The comment added by the user to this Super Chat event.|snippet.superChatDetails.userComment|
|isOwnner|bool|This value indicates whether the author is the owner of the live chat.|authorDetails.isChatOwner|

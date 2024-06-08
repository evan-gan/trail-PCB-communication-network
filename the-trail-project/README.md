# Architecture time!
The high-level goal of this project is to receive messages, display them on a screen, type messages and see a preview on the screen, and then send those messages. In our case to separate it up into three "subsystems." Each sub-system will interact with the other subsystems in a predefined way like the one I'm about to propose.
* There will be a function named `updateDisplay()` which will display the latest messages in the `history` array.
* Every time a message is received it will be fed into a function named `receivedMSG(MSG)`. This function will add the message to a `history` array & call the `updateDisplay()` function.
* A variable named `MSG_Draft` will be set & updated by the keyboard subsystem to store the message the user is currently typing. A function named `updateDisplay()`  will be called every time the draft is updated so that the display can be updated accordingly.
* A function named `sendDraft()` which will: 
    1. Send the drafted message with `sendMSG(MSG)` which will send a message over LoRa
    2. Add the message to the `history` array
    3. Call `updateDisplay()` so the display will show the new message
    4. Delete the contents of `MSG_Draft`

# Summery: Who will do what & how:
* I (@Evan) will implement the `sendDraft()`, and `receivedMSG(MSG)` functions
* @Cosmin (who is working on the display) will implement the `updateDisplay()` function which will display the contents of the `history` array the fit on the screen & the `MSG_Draft`.
* @j will implement the `MSG_Draft` variable setter which will call `updateDisplay()` every time it is modified with input from the keyboard.
* @Alex/@krisk will implement the `sendMSG(MSG)` function which will send the passed in text & when messages are received have them fed into the `receivedMSG(MSG)` function.

Please read all of the above! I spent 45 min writing it & it's important. If you have any questions or feel this structure could be improved for simplicity, message me on slack!

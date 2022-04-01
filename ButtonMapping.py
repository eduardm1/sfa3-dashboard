from inputs import get_gamepad
import datetime
import csv
import asyncio
import json

class ButtonMapping:

    def __init__(self, client):

        filename = r'./' + datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S') + '2st.csv'
        active_buttons = []
        self.filename = filename
        self.active_buttons = active_buttons
        self.client = client
        self.t_start_buttonE = 0
        self.t_start_buttonN = 0
        self.t_start_buttonS = 0
        self.t_start_buttonW = 0
        self.message = {}
        self.buttonPushed = 0
        self.t_start_bumperL = 0
        self.t_start_bumberR = 0
        self.buttonName = ""
        self.t_start_dpadD = 0
        self.t_start_dpadU = 0
        with open(self.filename, 'w', newline='') as csvfile:
            datatitlenames = ['Type', 'SpecifiedButton', 'Pressed', 'TimePressed']
            thewriter = csv.DictWriter(csvfile, fieldnames=datatitlenames)
            thewriter.writeheader()
            while True:
                time = datetime.datetime.now().time()
                events = get_gamepad()

                for event in events:
                    ################# Button group right #################

                    asyncio.run(self.rightBlockPress(event,thewriter))

                    # If button is released
                    asyncio.run(self.rightBlockReleased(event, thewriter))

                    #################### Upper button group ####################

                    asyncio.run(self.bumperPressed(event, thewriter))

                    asyncio.run(self.bumperReleased(event, thewriter))

                    #################### Button group left ####################

                    eventCode = event.code
                    # If button is pressed
                    asyncio.run(self.dPadPressed(event, eventCode, thewriter))

                    # If button is released
                    asyncio.run(self.dPadRelease(event, eventCode, thewriter))

                csvfile.flush()

    async def moves(self, event):
        if event.state == 0 and event.ev_type != "Sync":
            if event.code == 

    async def dPadRelease(self, event, eventCode, thewriter):
        if event.ev_type != "Sync" and event.state == 0:

            if eventCode == 'ABS_HAT0X':
                if self.buttonName == 'DPAD_LEFT':
                    t_stop_dpadL = event.timestamp
                    time_button_pressed = t_stop_dpadL - self.t_start_dpadL
                    print(event.ev_type, self.buttonName, event.state, time_button_pressed)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state,
                                    'TimePressed': time_button_pressed}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)
                else:
                    t_stop_dpadR = event.timestamp
                    self.buttonName = 'DPAD_RIGHT'
                    time_button_pressed = t_stop_dpadR - self.t_start_dpadR
                    print(event.ev_type, self.buttonName, event.state, time_button_pressed)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state,
                                    'TimePressed': time_button_pressed}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)

            elif eventCode == 'ABS_HAT0Y':

                if self.buttonName == 'DPAD_UP':
                    t_stop_dpadU = event.timestamp
                    self.buttonName = 'DPAD_UP'
                    time_button_pressed = t_stop_dpadU - self.t_start_dpadU
                    print(event.ev_type, self.buttonName, event.state, time_button_pressed)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state,
                                    'TimePressed': time_button_pressed}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)
                else:
                    t_stop_dpadD = event.timestamp
                    self.buttonName = 'DPAD_DOWN'
                    time_button_pressed = t_stop_dpadD - self.t_start_dpadD
                    print(event.ev_type, self.buttonName, event.state, time_button_pressed)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state,
                                    'TimePressed': time_button_pressed}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)

    async def dPadPressed(self, event, eventCode, thewriter):
        if event.ev_type != "Sync" and event.state == -1 or event.state == 1:

            if eventCode == 'ABS_HAT0X':
                if event.state == -1:
                    self.t_start_dpadL = event.timestamp
                    self.buttonName = 'DPAD_LEFT'
                    print(event.ev_type, self.buttonName, event.state)
                    self.message = {'Type': event.ev_type,
                         'SpecifiedButton': self.buttonName,
                         'Pressed': event.state}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)

                else:
                    self.t_start_dpadR = event.timestamp
                    self.buttonName = 'DPAD_RIGHT'
                    print(event.ev_type, self.buttonName, event.state)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)

            elif eventCode == 'ABS_HAT0Y':

                if event.state == -1:
                    self.t_start_dpadU = event.timestamp
                    self.buttonName = 'DPAD_UP'
                    print(event.ev_type, self.buttonName, event.state)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)
                else:
                    self.t_start_dpadD = event.timestamp
                    self.buttonName = 'DPAD_DOWN'
                    print(event.ev_type, self.buttonName, event.state)
                    self.message = {'Type': event.ev_type,
                                    'SpecifiedButton': self.buttonName,
                                    'Pressed': event.state}
                    await self.client.sendMessage(json.dumps(self.message))
                    thewriter.writerow(self.message)

    async def bumperReleased(self, event, thewriter):
        # If button is released
        if event.state == 0 and event.ev_type != "Sync":

            if event.code == 'BTN_TL':
                t_stop_bumperL = event.timestamp
                time_button_pressed = t_stop_bumperL - self.t_start_bumperL

                if event.code == 'BTN_TL':
                    self.buttonPushed = "BUMPER LEFT"

                print(event.ev_type, self.buttonPushed, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state,
                                'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_TR':
                t_stop_bumperR = event.timestamp
                time_button_pressed = t_stop_bumperR - self.t_start_bumberR

                if event.code == 'BTN_TR':
                    buttonPushed = "BUMPER RIGHT"

                print(event.ev_type, buttonPushed, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state,
                                'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

    async def bumperPressed(self, event, thewriter):
        # If button is pressed
        if event.state == 1 and event.ev_type != "Sync":
            if event.code == 'BTN_TL':
                self.t_start_bumperL = event.timestamp

                if event.code == 'BTN_TL':
                    self.buttonPushed = "BUMPER LEFT"

                print(event.ev_type, self.buttonPushed, event.state)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_TR':
                t_start_bumberR = event.timestamp

                if event.code == 'BTN_TR':
                    buttonPushed = "BUMPER RIGHT"

                print(event.ev_type, buttonPushed, event.state)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

    async def rightBlockReleased(self, event, thewriter):
        if event.state == 0 and event.ev_type != "Sync":

            if event.code == 'BTN_SOUTH':
                t_stop_buttonS = event.timestamp
                time_button_pressed = t_stop_buttonS - self.t_start_buttonS
                print(event.ev_type, event.code, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                     'SpecifiedButton': event.code,
                     'Pressed': event.state,
                     'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_WEST':
                t_stop_buttonW = event.timestamp
                time_button_pressed = t_stop_buttonW - self.t_start_buttonW
                square_pressed = 0
                print(event.ev_type, event.code, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state,
                                'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_NORTH':
                t_stop_buttonN = event.timestamp
                time_button_pressed = t_stop_buttonN - self.t_start_buttonN
                print(event.ev_type, event.code, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state,
                                'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_EAST':
                t_stop_buttonE = event.timestamp
                time_button_pressed = t_stop_buttonE - self.t_start_buttonE
                print(event.ev_type, event.code, event.state, time_button_pressed)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state,
                                'TimePressed': time_button_pressed}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

    async def rightBlockPress(self, event, thewriter):
        # If button is being pressed
        if event.state == 1 and event.ev_type != "Sync":
            if event.code == 'BTN_SOUTH':
                self.t_start_buttonS = event.timestamp
                print(event.ev_type, event.code, event.state)
                self.message = {'Type': event.ev_type,
                     'SpecifiedButton': event.code,
                     'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_WEST':
                self.t_start_buttonW = event.timestamp
                print(event.ev_type, event.code, event.state)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_NORTH':
                self.t_start_buttonN = event.timestamp
                print(event.ev_type, event.code, event.state)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

            if event.code == 'BTN_EAST':
                self.t_start_buttonE = event.timestamp
                print(event.ev_type, event.code, event.state)
                self.message = {'Type': event.ev_type,
                                'SpecifiedButton': event.code,
                                'Pressed': event.state}
                await self.client.sendMessage(json.dumps(self.message))
                thewriter.writerow(self.message)

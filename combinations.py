import datetime
import csv


class ControllerCombinations():

    # initialisation
    def __init__(self):
        active_buttons = []  # List of buttons being pushed in simulaneously
        self.filename = 'C:\\Users\\janva\\PycharmProjects\\pythonProject\\2021-03-17_1701372st.csv'  # Name of .csv file to read in
        self.length_of_file = 0
        self.active_buttons = active_buttons  # self.active_buttons is now the list of active_buttons
        self.left_joystick_rotation, self.right_joystick_rotation = 'CENTER', 'CENTER'  # joystick rotations start at neutral (needed a value)
        self.next_row_counter = 0  # Counter on which row of the .csv the program is
        self.next_pushed_button_counter = 0  # Keeps track of the next button input with a state of 1
        self.previous_timestamp_dpad = datetime.time(0, 0,
                                                     0)  # Previous DPAD button pressed time to see if there's a change of tactics (short time between pressing the buttons if chanching tactics)
        self.previous_pressed_dpad = ''  # Previous DPAD button being pushed to see which tactics combo is being pushed
        self.tactic_counter = 0  # Counts which tactic is being used (-2 = Defending -1 = low defending 0 = neutral  1 = low attacking  2 = attacking
        self.in_tactics_menu_up = False  # If the DPAD UP button is pushed, upper tactics menu is shown
        self.in_tactics_menu_down = False  # If the DPAD DOWN button is pushed, down tactics menu is shown
        self.in_tactics_menu_left_right = False  # If the DPAD LEFT or RIGHT button is pushed, left or right tactics menu is shown
        self.already_in_tactics_menu = False  # Checks if a tactis menu is already openend
        self.joystick_counter = 0  # Checks how many joystick movements is being used between timed shots
        self.button_being_tapped = False

    # Appends or removes buttons that are pressed or not pressed anymore from csv file
    def buttonsPressedList(self):

        # Initialise variables (I use splitlines to get rid of EOL characters)
        row = list(open(self.filename).read().splitlines())
        self.length_of_file = len(row)

        # Skip first line in .csv which is the column names and not actual data, plus row counter since the first line is skipped
        iter_row = iter(row)
        self.next_row_counter += 1
        next(iter_row)

        with open('combinations_2st.csv', 'w', newline='') as csvfile:
            datatitlenames = ['Action', 'TimeOfAction']
            thewriter = csv.DictWriter(csvfile, fieldnames=datatitlenames)
            thewriter.writeheader()

            for fields in iter_row:
                # Stop increasing the next row counter when end of file
                if self.next_row_counter < self.length_of_file - 1:
                    self.next_row_counter += 1

                # Set data from .csv file
                field = fields.split(',', 3)
                button = field[1]
                button_state = field[2]
                button_timestamp = datetime.datetime.strptime(field[3], '%H:%M:%S.%f').time()

                # If button is pressed
                if button_state == '1' or button_state == '-1' or button_state == 'PUSHED':

                    # See if the button is being tapped or hold (for defense purposes)

                    # See if a timed action (Fake pass, fake shot etc.) happend
                    if button == 'BTN_NORTH' or button == 'BTN_EAST' or button == 'BTN_SOUTH' or button == 'BTN_WEST':
                        timed_action = self.timed_combinations(row, button_timestamp)
                        # If a timed action happend, skip over the rows (already been read and appended by timed_combination function)
                        # and increase the (next) row counter to read the right row (the -1 means current row instead of +1 next row)
                        # If it's not a timed action you can check to see if the current button is being pressed long or tapped
                        # If it's a timed action with the last button being pressed long then the timed_combination class takes care of it
                        if timed_action == True:
                            timed_action = False
                            while self.next_row_counter - 1 != self.joystick_counter:
                                self.next_row_counter += 1
                                next(iter_row)
                            self.joystick_counter = 0
                        else:
                            self.button_being_tapped = self.buttonTappedOrHold(button, row, button_timestamp,
                                                                               self.next_row_counter)

                    # Append button and check if there's a combination
                    self.active_buttons.append(button)
                    action = self.buttonCombinations()

                    # If DPAD button is pressed change tactics, else add to active button list
                    if button == 'DPAD_LEFT' or button == 'DPAD_UP' or button == 'DPAD_RIGHT' or button == 'DPAD_DOWN':
                        # if self.previous_timestamp_dpad has never been set
                        if self.next_row_counter == 1:
                            self.previous_timestamp_dpad = button_timestamp
                        # Change tactics according to button input
                        action = self.changeTactics(button, button_timestamp)

                    if action != '' and action is not None:
                        thewriter.writerow(
                            {'Action': action,
                             'TimeOfAction': button_timestamp})

                    csvfile.flush()

                # Set joystick rotation if it ain't centered then check if it's a skillmove or other combination
                if button == 'JOYSTICK_LEFT' or button == 'JOYSTICK_RIGHT':
                    joystick_side = button
                    joystick_rotation = button_state

                    if joystick_side == 'JOYSTICK_LEFT':
                        self.left_joystick_rotation = joystick_rotation
                        if joystick_rotation != 'CENTER':
                            self.buttonCombinations()
                    elif joystick_side == 'JOYSTICK_RIGHT':
                        self.right_joystick_rotation = joystick_rotation
                        if joystick_rotation != 'CENTER':
                            self.buttonCombinations()

                # If button is released
                if button_state == '0' or button_state == 'NEUTRAL':
                    if button in self.active_buttons:
                        self.active_buttons.remove(button)

    def buttonTappedOrHold(self, button_being_pressed, row, button_timestamp, start_line):

        for button in range(start_line, self.length_of_file):
            button_line = row[button].split(',', 3)

            button_name = button_line[1]
            button_action_state = button_line[2]
            button_action_timestamp = datetime.datetime.strptime(button_line[3], '%H:%M:%S.%f').time()

            if button_name == button_being_pressed and button_action_state == '0':
                delta_time = datetime.datetime.combine(datetime.date.today(),
                                                       button_action_timestamp) - datetime.datetime.combine(
                    datetime.date.today(), button_timestamp)

                if delta_time.microseconds < 500000 and delta_time.seconds < 1:
                    return True
                else:
                    return False

    # Function to change the tactics using the DPAD button (timed action)
    def changeTactics(self, button, timestamp_datetime):
        button_pressed = button

        # If here for the first time, set empty variables
        if datetime.time.strftime(self.previous_timestamp_dpad,
                                  '%H:%M:%S') == '00:00:00' and self.previous_pressed_dpad == '':
            self.previous_pressed_dpad = button
            self.previous_timestamp_dpad = timestamp_datetime

        # Calculate the time betweens previous DPAD button and the new DPAD button and update the previous timestamp with the newer one
        delta_time = datetime.datetime.combine(datetime.date.today(), timestamp_datetime) - datetime.datetime.combine(
            datetime.date.today(), self.previous_timestamp_dpad)
        self.previous_timestamp_dpad = timestamp_datetime

        # Reset variables if there was no DPAD input in 2.5 seconds (uptime of the tactics menu)
        if delta_time.seconds > 2.5:
            self.in_tactics_menu_up = False
            self.in_tactics_menu_left_right = False
            self.in_tactics_menu_down = False
            self.already_in_tactics_menu = False

        # When DPAD UP or DPAD DOWN is pressed set menu open to True, and clear input button (so tactics don't get changed immediatly)
        if button_pressed == 'DPAD_UP' and self.in_tactics_menu_up == False and self.already_in_tactics_menu == False:
            self.in_tactics_menu_up = True
            self.already_in_tactics_menu = True
            button_pressed = ''
        elif button_pressed == 'DPAD_DOWN' and self.in_tactics_menu_down == False and self.already_in_tactics_menu == False:
            self.in_tactics_menu_down = True
            self.already_in_tactics_menu = True
            button_pressed = ''
        elif (
                button_pressed == 'DPAD_LEFT' or button_pressed == 'DPAD_RIGHT') and self.in_tactics_menu_left_right == False and self.already_in_tactics_menu == False:
            self.in_tactics_menu_left_right = True
            self.already_in_tactics_menu = True
            button_pressed = ''

        # If the tactics menu DPAD UP is active, change tactics
        if delta_time.seconds < 2.5 and self.in_tactics_menu_up == True:

            if button_pressed == 'DPAD_UP':
                return ('Get In The Box')
            elif button_pressed == 'DPAD_RIGHT':
                return ('Attacking Full Backs')
            elif button_pressed == 'DPAD_DOWN':
                return ('Extra Striker')
            elif button_pressed == 'DPAD_LEFT':
                return ('Hug Sideline')

            self.previous_pressed_dpad = button

        # If the tactics menu DPAD DOWN is active, change tactics
        if delta_time.seconds < 2.5 and self.in_tactics_menu_down == True:

            if button_pressed == 'DPAD_UP':
                return ('Striker Drop Back')
            elif button_pressed == 'DPAD_RIGHT':
                return ('Team Press')
            elif button_pressed == 'DPAD_DOWN':
                return ('Offside Trap')
            elif button_pressed == 'DPAD_LEFT':
                return ('Overload Ball Side')

            self.previous_pressed_dpad = button

        if delta_time.seconds < 2.5 and self.in_tactics_menu_left_right == True:
            if button_pressed == 'DPAD_LEFT' and self.tactic_counter > -2:
                self.tactic_counter -= 1
            if button_pressed == 'DPAD_RIGHT' and self.tactic_counter < 2:
                self.tactic_counter += 1

            if self.tactic_counter == -2:
                return ("Ultra Defensive")
            elif self.tactic_counter == -1:
                return ("Defensive")
            elif self.tactic_counter == 0:
                return ("Balanced")
            elif self.tactic_counter == 1:
                return ("Attacking")
            elif self.tactic_counter == 2:
                return ("Ultra Attacking")

        return ''

    # Check for timed shots
    def timed_combinations(self, row, button_timestamp):

        for timed_button in range(self.next_row_counter, self.length_of_file):
            timed_action = row[timed_button].split(',', 3)

            timed_action_button = timed_action[1]
            timed_action_button_state = timed_action[2]
            timed_action_timestamp = datetime.datetime.strptime(timed_action[3], '%H:%M:%S.%f').time()

            delta_time = datetime.datetime.combine(datetime.date.today(),
                                                   timed_action_timestamp) - datetime.datetime.combine(
                datetime.date.today(), button_timestamp)

            if delta_time.seconds < 0.7:
                # If the button has a state of 1 set the time to calculate the delta time to see if the action is in time
                if timed_action_button_state == '1':
                    if timed_action_button == 'BTN_EAST' and delta_time.microseconds < 500000:
                        self.button_being_tapped = self.buttonTappedOrHold(timed_action_button, row,
                                                                           timed_action_timestamp, timed_button)
                        self.joystick_counter = timed_button
                        self.active_buttons.append(timed_action_button)
                        return True
                    if timed_action_button == 'BTN_SOUTH' and delta_time.microseconds < 500000:
                        self.button_being_tapped = self.buttonTappedOrHold(timed_action_button, row,
                                                                           timed_action_timestamp, timed_button)
                        self.joystick_counter = timed_button
                        self.active_buttons.append(timed_action_button)
                        return True
                    if timed_action_button == 'BTN_WEST' and delta_time.microseconds < 500000:
                        self.button_being_tapped = self.buttonTappedOrHold(timed_action_button, row,
                                                                           timed_action_timestamp, timed_button)
                        self.joystick_counter = timed_button
                        self.active_buttons.append(timed_action_button)
                        return True
                    if timed_action_button == 'BTN_NORTH' and delta_time.microseconds < 500000:
                        self.button_being_tapped = self.buttonTappedOrHold(timed_action_button, row,
                                                                           timed_action_timestamp, timed_button)
                        self.joystick_counter = timed_button
                        self.active_buttons.append(timed_action_button)
                        return True
            else:
                return False

    # set booleans to true and see if any combinations are being pressed
    def buttonCombinations(self):

        in_possesion = True

        # in posession and attacking
        while in_possesion:
            if 'BTN_TL' in self.active_buttons and 'BTN_TR' in self.active_buttons and self.left_joystick_rotation != 'CENTER':
                return ("Strafe Dribble (Lock Face Angle)")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_TR' in self.active_buttons and 'BTN_EAST' in self.active_buttons:
                return ("Low Shot/Downward Header")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_TR' in self.active_buttons and 'BTN_WEST' in self.active_buttons:
                return ("Whipped Cross")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_EAST' in self.active_buttons:
                return ("Chip Shot")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_NORTH' in self.active_buttons:
                return ("Lobbed Through Pass")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_SOUTH' in self.active_buttons:
                return ("Pass and Go")
                break

            if 'BTN_TL' in self.active_buttons and 'BTN_WEST' in self.active_buttons:
                return ("High Lob / High Cross")
                break

            if 'BTN_TL' in self.active_buttons and self.left_joystick_rotation != 'CENTER':
                return ("Strafe Dribble")
                break

            if 'BTN_TR' in self.active_buttons and 'BTN_EAST' in self.active_buttons:
                return ("Finesse Shot")
                break

            if 'BTN_TR' in self.active_buttons and 'BTN_SOUTH' in self.active_buttons:
                return ("Driven Ground Pass")
                break

            # Timed
            if 'BTN_EAST' in self.active_buttons and 'BTN_SOUTH' in self.active_buttons:
                self.active_buttons.remove('BTN_EAST')
                return ('Fake Shot')
                break

            # Timed
            if 'BTN_WEST' in self.active_buttons and 'BTN_SOUTH' in self.active_buttons:
                self.active_buttons.remove('BTN_WEST')
                return ('Fake Pass')
                break

            # Timed (2x North button)
            if self.active_buttons.count('BTN_NORTH') == 2:
                self.active_buttons.remove('BTN_NORTH')
                return ('Lofted Through Pass')
                break

            # Timed (2x East button)
            if self.active_buttons.count('BTN_EAST') == 2:
                self.active_buttons.remove('BTN_EAST')
                return ('Timed Shot')
                break

            # Timed (2x South button)
            if self.active_buttons.count('BTN_SOUTH') == 2:
                self.active_buttons.remove('BTN_SOUTH')
                return ('lofted Ground Pass')
                break

            # Timed (2x West button and optional TR)
            if self.active_buttons.count('BTN_WEST') == 2 and 'BTN_TR' in self.active_buttons:
                self.active_buttons.remove('BTN_WEST')
                return ('Driven Ground Cross')
                break
            elif self.active_buttons.count('BTN_WEST') == 2:
                self.active_buttons.remove('BTN_WEST')
                return ('Ground Cross')
                break

            if 'BTN_TR' in self.active_buttons and 'BTN_NORTH' in self.active_buttons:
                return ('Threaded Through Pass')
                break

            if 'TRIGGER_LEFT' in self.active_buttons and 'TRIGGER_RIGHT' in self.active_buttons and self.left_joystick_rotation != 'CENTER':
                return ("Slow Dribble")
                break

            if 'TRIGGER_LEFT' in self.active_buttons and 'TRIGGER_RIGHT' in self.active_buttons:
                return ("Face Up Dribbling")
                break

            if 'TRIGGER_RIGHT' in self.active_buttons and self.right_joystick_rotation != 'CENTER':
                return ("First Touch/Knock-On")
                break

            if 'TRIGGER_LEFT' in self.active_buttons and self.left_joystick_rotation != 'CENTER':
                return ("Shield/Jockey")
                break
            elif 'TRIGGER_LEFT' in self.active_buttons and self.left_joystick_rotation == 'CENTER':
                return ('Protect Ball')
                break

            if 'TRIGGER_RIGHT' in self.active_buttons and self.right_joystick_rotation == 'CENTER' and self.left_joystick_rotation == 'CENTER':
                return ("Stop Ball")
                break

            if self.right_joystick_rotation != 'CENTER':
                return ('Skill Move')
                break

            if 'BTN_NORTH' in self.active_buttons:
                return ("Through Pass")
                break

            if 'BTN_EAST' in self.active_buttons:
                return ("Shoot/Volley/Header")
                break

            if 'BTN_SOUTH' in self.active_buttons:
                return ("Ground Pass/Header")
                break

            if 'BTN_WEST' in self.active_buttons:
                return ("Lob Pass/Cross/Header")
                break

            break

        while not in_possesion:

            # Timed (2x North button)
            if self.active_buttons.count('BTN_NORTH') == 2 and self.button_being_tapped == False:
                self.active_buttons.remove('BTN_NORTH')
                return ('Goalkeeper Cross Intercept')
                break

            if 'BTN_TR' in self.active_buttons and 'BTN_EAST' in self.active_buttons:
                return ("Instant Hard Tackle")
                break

            if self.right_joystick_rotation != 'CENTER':
                return ("Switch Player (Manual)")
                break

            if 'TRIGGER_LEFT' in self.active_buttons and 'TRIGGER_RIGHT' in self.active_buttons and self.button_being_tapped == False:
                return ("Running Jockey")
                break

            if 'TRIGGER_LEFT' in self.active_buttons and self.button_being_tapped == False:
                return ("Jockey/Grab & Hold")
                break
            elif 'TRIGGER_LEFT' in self.active_buttons and self.button_being_tapped == True:
                return ("Shoulder Challenge/Sealout")
                break

            if 'BTN_TL' in self.active_buttons and self.button_being_tapped == True:
                return ("Change Player")
                break

            if 'BTN_TR' in self.active_buttons and self.button_being_tapped == False:
                return ("Teammate Contain")
                break

            if 'BTN_NORTH' in self.active_buttons and self.button_being_tapped == False:
                return ("Rush Goalkeeper Out")
                break

            if 'BTN_EAST' in self.active_buttons and self.button_being_tapped == True:
                return ("Tackle/Push or Pull (When Chasing)")
                break
            elif 'BTN_EAST' in self.active_buttons and self.button_being_tapped == False:
                return ("Hard Tackle")
                break

            if 'BTN_SOUTH' in self.active_buttons and self.button_being_tapped == False:
                return ("Contain")
                break

            if 'BTN_WEST' in self.active_buttons:
                return ("Sliding Tackle")
                break

            break


button_combinations = ControllerCombinations()
button_combinations.buttonsPressedList()

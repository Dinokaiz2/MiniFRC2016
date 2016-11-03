import serial, time, pygame, sys, traceback

from DriverStation.AAfilledRoundedRect import AAfilledRoundedRect as RoundedRect

# How to create your own buttons:
# First, go to line 40.

class Main:
    def __init__(self):
        """This method runs as soon as the program starts."""
        success = False
        while not success:
            try:
                outgoing_bluetooth_port = input("COM Port: ")
                outgoing_bluetooth_port = int(outgoing_bluetooth_port)
                if not 0 <= outgoing_bluetooth_port <= 256:
                    raise ValueError()
            except ValueError as v:
                print("Invalid port! The COM port must be between 0 and 256.")
            else:
                success = True
        try:
            self.serial = serial.Serial("COM" + str(outgoing_bluetooth_port), 9600, timeout=None) # Access the COM port that sends data over Bluetooth
        except:
            print("ERROR: The port couldn't be opened. Is the Arduino connected? Try powering it off and on again.")
            input("Press enter/return to close the program.")
            sys.exit()
        else:
            print("Connected to robot!")
        pygame.init()
        self.clock = pygame.time.Clock() # Creates a timer to limit the framerate
        self.input_dirty = False # Is set to True only when the input changes so that we don't have to send stuff to the Arduino every frame.
        print("Driver Station started!")
        self.display = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("MiniFRC Driver Station")
        self.font = pygame.font.SysFont("helvetica", 45)
        self.error_font = pygame.font.SysFont("helvetica", 24)
        self.window_focused = True

        # Line 40: Here, you have to create a variable to hold the state of your button.
        # For example, for an arm, you might make a variable called arm that you set to 1 when it's up, -1 when it's down and 0 when it's in the middle.
        # This would look like: self.arm = 0
        # Once you've done that, go to line 48.

        self.speed = 0
        self.turn = 0

        # Line 48: Next, you're going to need to add it to the list of things to send to the Arduino.
        # To do this, add your variable name as a string to the thingsToSend list.
        # For example, if you wanted to add your arm variable to the list, it would look like:
        # self.thingsToSend = ["self.speed", "self.turn", "self.arm"]
        # Next, go to line 70.

        self.thingsToSend = ["self.speed", "self.turn"]
        
    def start_loop(self):
        """This method runs over and over until the program ends."""
        while True:
            self.clock.tick(60) # Limits the program to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.ACTIVEEVENT: # Detect if the window has lost focus
                    if event.state == 2:
                        self.window_focused = False
                    elif event.state == 6:
                        self.window_focused = True
                        
                # Line 70: Here, you're going to change the value of your variable when a key is pressed.
                # Where it says "Add your keydown statement here", you need to add an elif statement checking if the key is pressed.
                # If the key is pressed, you need to your variable's value to change and to change input_dirty so that the new
                # value will be sent to the Arduino.
                #
                # For example, if you had a variable called arm that should be set to 1 when the "R" key is pressed, you would do:
                # elif event.key == pygame.K_r:
                #     self.arm = 1
                #     self.input_dirty = True
                #
                # Next, go to line 102.
                
                
                elif event.type == pygame.KEYDOWN: # Check if a key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:   # If the key is the up arrow or W,
                        self.speed = 1                                          # Change the speed to 1
                        self.input_dirty = True                                 # Tell the program that an input changed
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.speed = -1
                        self.input_dirty = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.turn = 1
                        self.input_dirty = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.turn = -1
                        self.input_dirty = True
                    # Add your keydown statement here


                # Here, you need to make sure that the variable is also sent when the key is released.
                # You'll only need to do this step if you want the variable to change back after the key is released.
                # Where it says "Add your keyup statement here", you're going to add an elif statment that checks
                # if the key was released. If it was, you'll change your variable.
                #
                # Example: if you have a variable called arm and want to change it back to 0 once the "R" key
                # is released, you would do:
                # elif event.key == pygame.K_r:
                #     self.arm = 0
                #     self.input_dirty = True
                #
                # That's it! Your variable will now be sent over bluetooth to the Arduino.
                # Check the Robot.ino file in https://github.com/Dinokaiz2/MiniFRC2016/tree/master/Robot once
                # you've finished this to figure out how to use the data you've sent.
                    
                elif event.type == pygame.KEYUP:
                    if (((event.key == pygame.K_UP or event.key == pygame.K_w) and self.speed == 1) or
                       ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.speed == -1)):
                        self.speed = 0
                        self.input_dirty = True
                    elif (((event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.turn == 1) or
                         ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.turn == -1)):
                        self.turn = 0
                        self.input_dirty = True
                    # Add your keyup statement here

                
            if self.input_dirty: # Send the input to the Arduino if it's changed
                package = ""
                for var in self.thingsToSend:
                    var = eval(var)
                    package += str(var) + ','
                package = package[0:len(package)-1]
                print(package)
                package += 'a'
                self.serial.write(bytes(package, "utf-8"))
                
            self.input_dirty = False

            # Below this is GUI stuff
            self.display.fill((0, 110, 0))
            key_rect = pygame.Rect(10, 10, 180, 180)
            RoundedRect(self.display, key_rect, (50, 50, 50))
            dirs = []
            if self.speed == 1:
                dirs.append("Forward")
            elif self.speed == -1:
                dirs.append("Reverse")
            if self.turn == 1:
                dirs.append("Left")
            elif self.turn == -1:
                dirs.append("Right")
            if len(dirs) == 1:
                text = self.font.render(dirs[0], 1, (255, 255, 255))
                text_pos = (100 - (text.get_width() * 0.5), 100 - (text.get_height() * 0.5))
                self.display.blit(text, text_pos)
            elif len(dirs) == 2:
                top_text = self.font.render(dirs[0], 1, (255, 255, 255))
                top_text_pos = (100 - (top_text.get_width() * 0.5), 105 - (top_text.get_height()))
                bot_text = self.font.render(dirs[1], 1, (255, 255, 255))
                bot_text_pos = (100 - (bot_text.get_width() * 0.5), 95)
                self.display.blit(top_text, top_text_pos)
                self.display.blit(bot_text, bot_text_pos)
            if not self.window_focused:
                black_overlay = pygame.Surface((200, 200))
                black_overlay.set_alpha(128)
                black_overlay.fill((0, 0, 0))
                self.display.blit(black_overlay, (0, 0))
                top_text = self.error_font.render("WINDOW", 1, (255, 0, 0))
                mid_text = self.error_font.render("UNFOCUSED", 1, (255, 0, 0))
                bot_text = self.error_font.render("Click to restore", 1, (255, 0, 0))
                top_text_pos = (100 - top_text.get_width() * 0.5), 75 - (top_text.get_height())
                mid_text_pos = (100 - mid_text.get_width() * 0.5), 105 - (mid_text.get_height())
                bot_text_pos = (100 - bot_text.get_width() * 0.5), 150 - (bot_text.get_height())
                self.display.blit(top_text, top_text_pos)
                self.display.blit(mid_text, mid_text_pos)
                self.display.blit(bot_text, bot_text_pos)
            pygame.display.flip()
            
# This starts the program, probably don't need to touch anything below here.
if __name__ == "__main__":
    try:
        mainWindow = Main()
        mainWindow.start_loop()
    except Exception as e:
        traceback.print_stack()
        print("------------------------------------")
        traceback.print_exc()
        pygame.quit()
        sys.exit(0)

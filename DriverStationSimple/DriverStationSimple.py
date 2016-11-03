import serial, time, pygame, sys, traceback

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
            print("ERROR: The port couldn't be opened. Is the Arduino connected? Try unplugging and replugging it.")
            input("Press enter/return to close the program.")
            sys.exit()
        else:
            print("Connected to robot!")
        pygame.init()
        self.clock = pygame.time.Clock() # Creates a timer to limit the framerate
        self.speed = 0
        self.turn = 0
        self.input_dirty = False # Is set to True only when the input changes so that we don't have to send stuff to the Arduino every frame.
        print("Driver Station started!")
        self.display = pygame.display.set_mode((200, 200))
        pygame.display.set_caption("MiniFRC Driver Station")
        self.font = pygame.font.SysFont("helvetica", 45)
        self.error_font = pygame.font.SysFont("helvetica", 24)
        self.window_focused = True
        
    def start_loop(self):
        """This method runs over and over until the program ends."""
        while True:
            self.clock.tick(60) # Limits the program to 60 frames per second
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.ACTIVEEVENT: # Detect if the window has lost focus
                    print(event.state)
                    if event.state == 2:
                        self.window_focused = False
                    elif event.state == 6:
                        self.window_focused = True
                        
                # IF YOU'RE LOOKING TO ADD NEW BUTTONS, BELOW IS THE PLACE
                
                elif event.type == pygame.KEYDOWN: # Check if a key is pressed
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w: # If the key is the up arrow or W,
                        self.speed = 1                                        # Change the speed to 1
                        self.input_dirty = True                               # Tell the program that an input changed
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.speed = -1
                        self.input_dirty = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.turn = 1
                        self.input_dirty = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.turn = -1
                        self.input_dirty = True
                    
                elif event.type == pygame.KEYUP:
                    if (((event.key == pygame.K_UP or event.key == pygame.K_w) and self.speed == 1) or
                       ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.speed == -1)):
                        self.speed = 0
                        self.input_dirty = True
                    elif (((event.key ==  pygame.K_LEFT or event.key == pygame.K_a) and self.turn == 1) or
                         ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.turn == -1)):
                        self.turn = 0
                        self.input_dirty = True
            if self.input_dirty: # Send the input to the Arduino if it's changed
                package = str(self.turn) + ',' + str(self.speed) + 'a'
                self.serial.write(bytes(package, "utf-8"))
            self.input_dirty = False
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

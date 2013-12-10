import pygame


class Button():
    def __init__(self):
        self.flag = False
        self.rect = None

    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x, y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length // (len(text) * 0.7))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 3, text_color)
        surface.blit(myText, ((x + length / 2) - myText.get_width() / 2, (y + height / 2) - myText.get_height() / 2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):
        #for i in range(1,10):
        s = pygame.Surface((length, height))
        s.fill(color)
        #alpha = (255/(i+2))
        #if alpha <= 0:
        #    alpha = 1
        #s.set_alpha(alpha)
        pygame.draw.rect(s, color, (x, y, length, height), width)
        #surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x, y, length, height), 0)
        #pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)
        return surface

    def pressed(self, mouse_cursor):
        if self.rect.colliderect(mouse_cursor):
            return True
        else:
            return False


class TextRectException():
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException  # "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        #if accumulated_height + font.size(line)[1] >= rect.height:
            #raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException  # "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface


def update_buttons(mouse_cursor,
                  LogStack, LogButton, CloseLogButton,
                  DetailsButton, CloseDetailsButton,
                  HelpButton, CloseHelpButton,
                  MissionButton, CloseMissionButton,
                  MissionCoup, MissionGI, MissionDip,
                  MissionAssas, MissionSubvert, MissionScavenge,
                  MissionCamp, MissionRebelion):

    #If the Log button is pressed, then display the window
    if LogButton.pressed(mouse_cursor):
        LogButton.flag = True
    elif CloseLogButton.pressed(mouse_cursor):
        LogButton.flag = False
    elif DetailsButton.pressed(mouse_cursor):
        DetailsButton.flag = True
    elif CloseDetailsButton.pressed(mouse_cursor):
        DetailsButton.flag = False
    elif HelpButton.pressed(mouse_cursor):
        HelpButton.flag = True
    elif CloseHelpButton.pressed(mouse_cursor):
        HelpButton.flag = False
    elif MissionButton.pressed(mouse_cursor):
        MissionButton.flag = True
    elif CloseMissionButton.pressed(mouse_cursor):
        MissionButton.flag = False
    elif MissionCoup.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Coup Mission Selected")
    elif MissionGI.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Gather Information Mission Selected")
    elif MissionDip.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Diplomacy Mission Selected")
    elif MissionAssas.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Assasination Mission Selected")
    elif MissionSubvert.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Subvert Troops Mission Selected")
    elif MissionScavenge.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Scavenge Mission Selected")
    elif MissionCamp.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Start Rebel Camp Mission Selected")
    elif MissionRebelion.pressed(mouse_cursor):
        #Send off request to Backend
        LogStack.insert(0, "Start/Stop Rebelion Mission Selected")


#Draw menus and buttons based off of flag values
def draw_buttons(screen, selectionlist,
                LogStack, LogButton, CloseLogButton,
                DetailsButton, CloseDetailsButton,
                HelpButton, CloseHelpButton,
                MissionButton, CloseMissionButton,
                MissionCoup, MissionGI, MissionDip,
                MissionAssas, MissionSubvert, MissionScavenge,
                MissionCamp, MissionRebelion):

    if(LogButton.flag == True):
        #If LogFlag is set, then display the text window
        #Format the output string
        if(len(LogStack) > 10):
            LogStack.pop()
        Log_Message = ""
        for item in LogStack:
            Log_Message = Log_Message + str(item) + "\n"
        log_font = pygame.font.Font(None, 15)
        log_rect = pygame.Rect((0, 650, 300, 150))
        rendered_text = render_textrect(Log_Message, log_font, log_rect, (216, 216, 216), (48, 48, 48), 0)
        screen.blit(rendered_text, log_rect.topleft)
        #Parameters:                 surface, color,       x,   y,  length, height, width, text,  text_color
        CloseLogButton.create_button(screen, (255, 0, 0), 285,  655,    10,    10,   10,    "X", (0, 0, 0))
    else:
        LogButton.create_button(screen, (0, 255, 0), 10,  750,  100,  30,   0,  "Log   ", (255, 255, 255))
    if(DetailsButton.flag == True):
        details_rect = pygame.Rect((724, 650, 300, 150))
        pygame.draw.rect(screen, (48, 48, 48), details_rect)
        #details_sub_rect = pygame.Rect((724, 635, 300, 135))
        #detailScreen = screen.subsurface(details_sub_rect)
        #tmpSel = selectionlist.sprites()

        #details_font = pygame.font.Font(None, 20)
        #rendered_text = render_textrect("Details Placeholder", details_font, details_rect, (216, 216, 216), (48, 48, 48), 0)
        #screen.blit(rendered_text, details_rect.midtop)
        #Parameters:                     surface, color,       x,   y,   length, height, width, text,       text_color
        CloseDetailsButton.create_button(screen, (255, 0, 0), 1010,  655,    10,    10,   10,    "X", (0, 0, 0))
    else:
        DetailsButton.create_button(screen, (0, 255, 0), 900,  750,    100,    30,   0,  "Details", (255, 255, 255))
    if(MissionButton.flag == True):
        mission_rect = pygame.Rect((330, 650, 350, 150))
        pygame.draw.rect(screen, (48, 48, 48), mission_rect)
        #Draw the mission select buttons
        #Parameters:              surface, color,       x,   y,   length, height, width, text,       text_color
        MissionCoup.create_button(screen, (0, 255, 0), 340,  665,    100,    30,   0,  "Coup   ", (255, 255, 255))
        MissionGI.create_button(screen, (0, 255, 0), 455,  665,    100,    30,   0,  "Gather Info", (255, 255, 255))
        MissionDip.create_button(screen, (0, 255, 0), 565,  665,    100,    30,   0,  "Diplomacy", (255, 255, 255))
        MissionAssas.create_button(screen, (0, 255, 0), 340,  715,    100,    30,   0,  "Assasination", (255, 255, 255))
        MissionSubvert.create_button(screen, (0, 0, 255), 455,  715,    100,    30,   0,  "Subvert ", (255, 255, 255))
        MissionScavenge.create_button(screen, (0, 0, 255), 565,  715,    100,    30,   0,  "Scavenge", (255, 255, 255))
        MissionCamp.create_button(screen, (0, 0, 255), 340,  755,    100,    30,   0,  "Start Camp", (255, 255, 255))
        MissionRebelion.create_button(screen, (0, 255, 0), 455,  755,    210,    30,   0,  "Start/Stop Rebelion", (255, 255, 255))
        CloseMissionButton.create_button(screen, (255, 0, 0), 665,  655,    10,    10,   10,    "X", (0, 0, 0))
    else:
        MissionButton.create_button(screen, (0, 255, 0), 475,  745,    100,    30,   20,  "Missions", (255, 255, 255))
    if(HelpButton.flag == True):
        Help_Message = "This text will change based on the current player phase"
        help_bg = pygame.Rect((0, 0, 300, 30))
        pygame.draw.rect(screen, (48, 48, 48), help_bg)
        help_font = pygame.font.Font(None, 15)
        help_rect = pygame.Rect((0, 20, 300, 280))
        rendered_text = render_textrect(Help_Message, help_font, help_rect, (216, 216, 216), (48, 48, 48), 0)
        screen.blit(rendered_text, help_rect.topleft)
        #Parameters:                 surface, color,       x,   y,  length, height, width, text,  text_color
        CloseHelpButton.create_button(screen, (255, 0, 0), 285,  5,    10,    10,   10,    "X", (0, 0, 0))
    else:
        HelpButton.create_button(screen, (0, 255, 0), 5,  5,  100,  30,   0,  "Help  ", (255, 255, 255))

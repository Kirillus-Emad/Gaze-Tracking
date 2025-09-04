# import cv2 as cv
# import numpy as np

# def draw_keyboard():

#     # Canvas size
#     KYBRD_WIDTH = 1200
#     KYBRD_HEIGHT = 600

#     # Create blank image
#     Keyboard = np.zeros((KYBRD_HEIGHT, KYBRD_WIDTH, 3), dtype='uint8')
    
#     return Keyboard

# # cv.imshow('key',draw_keyboard())
# # cv.waitKey(0)
# # keyboard=draw_keyboard()

# def get_letters():

#     en_letters_1=['q','w','e','r','t',
#                   'a','s','d','f','g',
#                   'z','x','c','v','>>',
#                   'CAPS','ARB','SYB','NUM'] 
    
#     en_letters_2=['y','u','i','o','p',
#                   'h','j','k','l','_',
#                   'v','b','n','m','<<',
#                   'CAPS','ARB','SYB','NUM']
    
#     ar_letters_1=['ض','ص','ث','ق','ف',
#                   'ش','س','ي','ب','ل',
#                   'ئ','ء','ؤ','ر','ى','>>',
#                   'ENG','SYB','NUM']
    
#     ar_letters_2=['غ','ع','ه','خ','ح',"ج","د",
#                   'ا','ت','ن','م','ك',
#                   "ط",'ة','و','ز',"ظ",
#                   '<<','ENG','SYB','NUM']
    
#     symbols_1=[',',':','[',']','{',
#              '}','(',')','&','^',
#              '%','$','#','@','!','>>',
#              'ENG','ARB','NUM']
             
#     symbols_2=['~','<','>','?',
#                '\\','-','_','|',
#                'ENG','ARB','NUM']
    
#     numbers=['0','1','2','3','4',
#              '5','6','7','8','9','=',
#              '+','/','*','-','.',
#              'ARB','ENG','SYMB']
    
#     return en_letters_1,len(en_letters_1),en_letters_2,len(en_letters_2),ar_letters_1,len(ar_letters_1),ar_letters_2,len(ar_letters_2),symbols_1,len(symbols_1),symbols_2,len(symbols_2),numbers,len(numbers)

# # en_letters_1=get_letters()


# # _,s1,_,s2,_,s3,_,s4,_,s5,_,s6,_,s7=get_letters()

# # print(max(s1,s2,s3,s4,s5,s6,s7))

# def letter(x,y,text,Keyboard,light):
    
#     KEY_WIDTH = 200
#     KEY_HEIGHT = 200
#     THK = 3
#     COLOR_KEY = (255, 255, 255)
    
#     if light is True:
#     # Draw rectangle (key)
#         cv.rectangle(Keyboard, (x + THK, y + THK), (x + KEY_WIDTH - THK, y + KEY_HEIGHT - THK), (255,255,255), -1)
#     else:
#         cv.rectangle(Keyboard, (x + THK, y + THK), (x + KEY_WIDTH - THK, y + KEY_HEIGHT - THK), (255,0,0), THK)
    
#     # Text settings
#     font_letter = cv.FONT_HERSHEY_PLAIN
#     Font_scale = 10
#     font_thk = 4

#     # Get text size
#     (text_width, text_height), baseline = cv.getTextSize(text, font_letter, Font_scale, font_thk)

#     # Compute center position for the text
#     text_x = x + (KEY_WIDTH - text_width) // 2
#     text_y = y + (KEY_HEIGHT + text_height) // 2  # text is aligned to the baseline, so adjust using height

#     # Draw text
#     cv.putText(Keyboard, text, (text_x, text_y), font_letter, Font_scale, (255,0,0), font_thk)

# # letter(0,0,'A')
# # letter(150,0,'B')
# # letter(300,0,'C')

# # draw first subset of english characters

# def draw_letters(en_letters_1,keyboard,letter_ind):

#     row=0
#     for y in range(0,401,200):
#         for x in range(0,801,200):
            
#             if row == letter_ind:
#                 light=True
#             else:
#                 light=False
            
#             letter(x,y,en_letters_1[row],keyboard,light)
                
#             row+=1
        

# # draw_letters(en_letters_1,keyboard,3)

# # # Show the result
# # cv.imshow('keyboard', keyboard)
# # cv.waitKey(0)
# # cv.destroyAllWindows()


################ chat gpt ###########333

from PIL import ImageFont, ImageDraw, Image
import arabic_reshaper
from bidi.algorithm import get_display
import cv2 as cv
import numpy as np

# # Constants
# KEY_WIDTH = 100
# KEY_HEIGHT = 100
# KEYS_PER_ROW = 10
# THK = 3  # Thickness

# Canvas size
KYBRD_WIDTH = 1200
KYBRD_HEIGHT = 600

def draw_keyboard():
    """Creates a blank keyboard canvas."""
    keyboard = np.zeros((KYBRD_HEIGHT, KYBRD_WIDTH, 3), dtype='uint8')
    return keyboard

def get_letters():
    """Returns various key layouts and their lengths."""
    en_letters_1 = ['q','w','e','r','t',
                    'a','s','d','f','g',
                    'z','x','c','v','>>','__',
                    'CAPS','ARB','SYB','NUM','<--'] # 5 * 4

    en_letters_2 = ['y','u','i','o','p',
                    'h','j','k','l','__',
                    'v','b','n','m','<<',
                    'CAPS','ARB','SYB','NUM','<--'] # 6 * 4

    ar_letters_1 = ['ض','ص','ث','ق','ف',
                    'ش','س','ي','ب','ل',
                    'ئ','ء','ؤ','ر','ى','__',
                    '>>','ENG','SYB','NUM','<--']   # 6 * 4

    ar_letters_2 = ['غ','ع','ه','خ','ح',"ج",
                    "د",'ا','ت','ن','م','ك',
                    "ط",'ة','و','ز',"ظ",'__',
                    '<<','ENG','SYB','NUM','<--']  # 6 * 4

    symbols_1 = [',',':','[',']','{',
                 '}','(',')','&','^',
                 '%','$','#','@','!','__',
                 '>>','ENG','ARB','NUM','<--']     # 6 * 4

    symbols_2 = ['~','<','>','?','\\',
                 '-','_','|','<<','__',
                 'ENG','ARB','NUM','<--']          # 6 * 4 

    numbers = ['0','1','2','3','4',
               '5','6','7','8','9',
               '=','+','/','*','-','__',
               '.','ARB','ENG','SYB','<--']      # 6 * 4

    return en_letters_1, en_letters_2, ar_letters_1, ar_letters_2, symbols_1, symbols_2, numbers

KEY_WIDTH = 200
KEY_HEIGHT = 150
THK = 3

def letter(x, y, text, keyboard, light):
    if light:
        cv.rectangle(keyboard, (x + THK, y + THK), (x + KEY_WIDTH - THK, y + KEY_HEIGHT - THK), (255,255,255), -1)
    else:
        cv.rectangle(keyboard, (x + THK, y + THK), (x + KEY_WIDTH - THK, y + KEY_HEIGHT - THK), (255,0,0), THK)

    keyboard_pil = Image.fromarray(cv.cvtColor(keyboard, cv.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(keyboard_pil)

    try:
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
    except:
        bidi_text = text

    font_path = "arial.ttf"  # Make sure this font supports Arabic
    font_size = 32
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Calculate text size
    try:
        bbox = draw.textbbox((0,0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        # fallback for older Pillow
        text_width, text_height = font.getsize(bidi_text)

    text_x = x + (KEY_WIDTH - text_width) // 2
    text_y = y + (KEY_HEIGHT - text_height) // 2

    draw.text((text_x, text_y), bidi_text, font=font, fill=(255, 0, 0))

    # Convert back to OpenCV image
    keyboard[:] = cv.cvtColor(np.array(keyboard_pil), cv.COLOR_RGB2BGR)


# def draw_letters(key_list, keyboard, highlight_index=None):
#     """Draws the full list of keys onto the keyboard canvas."""
#     for idx, key in enumerate(key_list):
#         row = idx // KEYS_PER_ROW
#         col = idx % KEYS_PER_ROW
#         x = col * KEY_WIDTH
#         y = row * KEY_HEIGHT
#         light = (highlight_index == idx)
#         letter(x, y, key, keyboard, light)

# def draw_letters(key_set,keyboard,letter_index):
#     size_key_set=len(key_set)
#     row=0

#     for y in range(0,401,150):
#         for x in range(0,1001,200):
#             if row < size_key_set:
#                 if row == letter_index:
#                     light=True
#                 else:
#                     light=False
                
#                 letter(x,y,key_set[row],keyboard,light)
                    
#                 row+=1
#             else:
#                 break

def draw_letters(key_set, keyboard, letter_index):
    size_key_set = len(key_set)
    cols = KYBRD_WIDTH // KEY_WIDTH
    rows = KYBRD_HEIGHT // KEY_HEIGHT

    total_keys = rows * cols

    for idx, key in enumerate(key_set):
        row = idx // cols
        col = idx % cols
        x = col * KEY_WIDTH
        y = row * KEY_HEIGHT

        light = (idx == letter_index)
        letter(x, y, key, keyboard, light)

# Example usage
if __name__ == "__main__":
    # Get all the keyboard layouts
    en_letters_1, en_letters_2, ar_letters_1, ar_letters_2, symbols_1, symbols_2, numbers = get_letters()

    # Choose any layout to display:
    keys_to_display = numbers  # Change this to test other layouts

    # Draw the keyboard
    keyboard = draw_keyboard()
    draw_letters(keys_to_display, keyboard,3)

    # Show the keyboard
    cv.imshow('Virtual Keyboard', keyboard)
    cv.waitKey(0)
    cv.destroyAllWindows()


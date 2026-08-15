from util.load_image import import_image, IMAGE_SCALE

alphabet = {}

def load_alphabet():
    chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9","colon","!"]
    for i in chars:
        alphabet[i] = import_image(f"resources/font/{i}.png")

def write_string(screen, string, x, y):
    old_x = x
    for char in string:
        if char == " ":
            x += 3 * IMAGE_SCALE
        elif char == "\n":
            x = old_x
            y += 11 * IMAGE_SCALE
        else:
            if char == ":":
                char_img = alphabet["colon"]
            else:
                char_img = alphabet[f"{char.upper()}"]
            screen.blit(char_img, (x, y))
            x += char_img.get_width() + IMAGE_SCALE
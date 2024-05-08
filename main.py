from src.common_imports import *

items = ss.gdrive()

# print the names of each item
for item in items:
    print(item['name'])
    print(item['mimeType'])
    print(item['id'])
    print()


# Create the main window
root = tk.Tk()
#root.attributes('-fullscreen', True)
root.geometry("1920x1080")
root.configure(background='black')
root.title('slideshow tool')

img_arr, img_files, panel = ss.loop(root)

x = 1
def move():
    global x
    if x == len(img_arr) + 1:
        x = 1
    if x == 1:
        panel.config(image=img_arr[x-1])
    else:
        panel.config(image=img_arr[x-1])
    x = x + 1
    print("current image = " + img_files[x-2])
    root.after(2000, move)

move()

root.mainloop()
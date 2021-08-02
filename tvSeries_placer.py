# Copyright (c) 2021 Chamith-Nimmitha
# Don't kang this 

"""

"""


import tkinter as tk
import tkinter.filedialog
import os
import re
import shutil

def undo(location,msg_text):
	"""
	This function move all files from the folders to root directory.

	:param location(str): Folder location where tv series episode folders are located.
	:param msg_text(StringVar) : notification frame message variable
	:return: None
	"""
	msg_text.set("")
	try:
		os.chdir(location)
	except FileNotFoundError as e:
		msg_text.set(e)
		return
	except Exception as e:
		msg_text.set("Location error")
		return

	cwd = os.getcwd()
	for path,dir,fi in os.walk(cwd):
		for f in fi:
			target = os.path.join(path, f)
			shutil.move(target,os.path.join(cwd,f))

	for dir in os.scandir(cwd):
		if(dir.is_dir()):
			shutil.rmtree(os.path.join(cwd,dir))

	msg_text.set("Successful...")


def placer(location,msg_text,season_flag, sub_flag,sub_folder):
	"""
	This function create folders for each episode and move relavant video file to relavent folder.Also this can create and place subtitles in correct folder.

	:param location(str): Folder location where tv series episodes are located.
	:param msg_text(str): notification frame message variable
	:param season_flag(bool): folder contains multiple seasons indicator
	:param sub_flag(bool): create a sub folder for each episode indicatior
	:param sub_folder(string): sub folder name

	:return: None;
	"""
	current_dir = os.getcwd()
	msg_text.set("")

	try:
		os.chdir(location)
	except FileNotFoundError as e:
		msg_text.set(e)
		return
	except Exception as e:
		msg_text.set("Location error")
		return

	ch_dir = os.getcwd()
	d = os.listdir()
	dirs = list()
	for x in d:
		if not os.path.isdir(x):
			dirs.append(x)

	len_dirs = len(dirs)

	if len_dirs == 0:
		msg_text.set(f"Nothing to do with \n {current_dir}  directory.\n(Current working directory.)")
		return
	try:
		x=0
		pattern1 = re.compile(r"[sS](\d\d|\d)(\.|x|-|_|\s)?[eE](\d\d|\d)")
		pattern2 = re.compile(r"[sS]?(\d\d|\d)(x|-|_|\s)[eE]?(\d\d|\d)")
		while(x < len(dirs)):
			x+=1
			result = pattern1.findall(dirs[x-1])
			if len(result) == 0:
				result = pattern2.findall(dirs[x-1])

			if len(result) > 0:
				season = f"Season {str(result[0][0]).zfill(2)}"
				new_dir = f"S{str(result[0][0]).zfill(2)}E{str(int(result[0][len(result[0])-1])).zfill(2)}"
				if(sub_flag):
					sub_dir = os.path.join(new_dir, sub_folder)
				else:
					sub_dir = new_dir

				if(season_flag):
					new_dir = os.path.join(season,new_dir)
					sub_dir = os.path.join(season,sub_dir)

				try:
					if(sub_flag):
						os.makedirs(sub_dir)
					else:
						os.makedirs(new_dir)

				except Exception:
					pass
				finally:
					if(os.path.splitext(dirs[x-1])[1] != ".srt"):
						os.rename(os.path.join(ch_dir,dirs[x-1]),os.path.join(os.path.join(ch_dir,new_dir),dirs[x-1]))
					else:
						os.rename(os.path.join(ch_dir,dirs[x-1]),os.path.join(os.path.join(ch_dir,sub_dir),dirs[x-1]))
					dirs.remove(dirs[x-1])
					x-=1
		if(len(dirs) > 0):
			msg_text.set(f"{len(dirs)} file(s) not like tv series file(s).")

		msg_text.set(f"{len_dirs-len(dirs)} file(s) successfully placed...\n{msg_text.get()}")

	except Exception as e:
		msg_text.set(f"{e} in \n {current_dir}  directory.\n(Current working directory.)")


def main():
	root = tk.Tk(className=" Tv Series Manupulator")
	canvas = tk.Canvas(root,width=800,height=600,bg="#99ccff")
	canvas.pack()

	#frame for user inputs
	l_frame = tk.Frame(canvas,bg="#999",bd=20)
	l_frame.place(relx=0.05,rely=0.05,relwidth=0.9,relheight=0.45)

	# for file location
	l_label = tk.Label(l_frame,bg="#eee",text="File location",fg="black")
	l_label.place(relwidth=0.2,relheight=0.15)

	# for show selected location
	l_label_show_text = tk.StringVar()
	l_label_show_text.set("");
	l_label_show = tk.Label(l_frame, textvariable=l_label_show_text, bg="#eee",text="",fg="black")
	l_label_show.place(relx =0.215,relwidth=0.4,relheight=0.15)

	# get tv searies file location
	def open_file():
		filename = tk.filedialog.askdirectory()
		l_label_show_text.set(filename)
	l_button = tk.Button(l_frame, text="Select folder", bg="#426367", fg="white", command=open_file)
	l_button.place(relx =0.630,relwidth=0.15,relheight=0.15)

	# for season checkbox
	seasonChkVar = tk.BooleanVar()
	seasonChkVar.set(False)
	l_season_check = tk.Checkbutton(l_frame, text="This contain\n multiple seasons.",var=seasonChkVar)
	l_season_check.place( relx= 0.8,relwidth=0.2)


	#for subtitle
	l_sub_label = tk.Label(l_frame, bg="#eee", text="Subtitle folder", fg="black")
	l_sub_label.place( rely=0.415, relwidth=0.2, relheight=0.15)
	chkVar = tk.BooleanVar()
	chkVar.set(False)
	l_sub_check = tk.Checkbutton(l_frame, text="want sub folder.", var=chkVar)
	l_sub_check.place( rely=0.44, relx= 0.215, relwidth=0.2)
	l_sub_box = tk.Entry(l_frame, bg="#D1EEEE", fg="black", bd=5,justify="center")
	l_sub_box.insert(0,"example:- sinhala_sub or eng_sub")
	l_sub_box.place( relx=0.45, rely=0.415, relwidth=0.45, relheight=0.15)

	# buttons for operations
	l_button_undo = tk.Button(l_frame,text="Undo", command=lambda: undo(l_label_show_text.get(),msg_text))
	l_button_undo.place(rely= 0.75 ,relx=0.25,relwidth=0.2,relheight=0.15)
	l_button_place = tk.Button(l_frame,text="Place", command=lambda: placer(l_label_show_text.get(),msg_text, seasonChkVar.get(), chkVar.get(), l_sub_box.get()))
	l_button_place.place(rely= 0.75 ,relx=0.5,relwidth=0.2,relheight=0.15)

	#end input frame


	#message frame begin
	msg_text = tk.StringVar()

	# text variable for notifications
	msg_text.set("""
	This application can create folders for each episodes and put videos and subtitiles in to compatible folder.
	OR
	Undo this proccess.

	File location : Select where tv series is located.

	This contain multiple season : check this, If file loaction contain more than one season.

	Want sub folder : Check this if you want subtitle folder for each episode.

	If this checked, then you must specify sub folder name.

	UNDO : move out all files to root(given file location) folder.
	Place : Create and place tv series episodes in correct folder.

		""")

	msg_frame = tk.Frame(canvas,bg="red",bd=10)
	msg_frame.place(relx=0.05,rely=0.5,relwidth=0.9,relheight=0.45)

	msg_label = tk.Label(msg_frame,textvariable=msg_text)
	msg_label.place(relwidth=1,relheight=1)
	#message frame begin
	root.mainloop()

if __name__ == '__main__':
	main()

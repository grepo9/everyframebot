import os, re, glob, sqlite3


eps = glob.glob("*.mp4")

fps = 1

os.mkdir('frames')


movie_name = 'Akira'

out_path = f'./frames'
if not os.path.isdir(out_path):
    os.mkdir(out_path)


os.system(f'ffmpeg -i "{eps[0]}" -vf "fps={fps},scale=640:360" {out_path}/{movie_name}%d.jpg')



connection = sqlite3.connect("framebot.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS movie (movie TEXT, frames INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS bot (movie TEXT, last_frame INTEGER)")

cursor.execute("INSERT OR IGNORE INTO movie (movie, frames) VALUES (?, ?)", (movie_name, len(glob.glob(f"{out_path}/{movie_name}*.jpg"))))
cursor.execute("INSERT OR IGNORE INTO bot (movie, last_frame) VALUES (?, ?)", (movie_name, 0))
connection.commit()



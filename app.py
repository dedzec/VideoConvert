# ==== Importing all the necessary libraries
from tkinter import *
from tkinter import filedialog
from pydub import AudioSegment
from pydub.utils import make_chunks
import os
import moviepy.editor as mp
import speech_recognition as sr

# ==== creating main class
class VideoAudioConverter:
    # ==== creating gui window
    def __init__(self, root):
        self.root = root
        self.root.title("VIDEO-CONVERTER")
        self.root.geometry('500x200')
        # self.bg = ImageTk.PhotoImage(file="bg_image.jpg")
        # Label(self.root, image=self.bg).place(x=0, y=0)

        Button(self.root,text="Browse Files",font=("times new roman", 15),command=self.browse).place(x=20, y=20)

    # ==== browse data from system
    def browse(self):
        self.file_name = filedialog.askopenfilename(title="Select a File", filetypes=(("Video files", "*.mp4*"),))

        Label(self.root, text=os.path.basename(self.file_name), font=("times new roman", 15), bg="blue").place(x=150, y=30)

        Label(self.root, text='Processing...', font=("times new roman", 30)).place(x=20, y=80)
        
        self.convert(os.path.basename(self.file_name))
        
        self.process_audio(os.path.basename(self.file_name))
        
        Label(self.root, text='Completed!!', font=("times new roman", 30)).place(x=20, y=140)

    # ==== convert video to audio
    def convert(self, path):
        clip = mp.VideoFileClip(r'{}'.format(path))
        clip.audio.write_audiofile(r'{}wav'.format(path[:-3]))

    # ==== convert audio to text
    def process_audio(self, path):
        txtf = open("the_audio.txt", "w+")
        myaudio = AudioSegment.from_wav(r'{}wav'.format(path[:-3]))
        chunks_length_ms = 8000
        chunks = make_chunks(myaudio, chunks_length_ms)
        for i, chunk in enumerate(chunks):
            chunkName = './chunked/'+path+"_{0}.wav".format(i)
            print('I am exporting', chunkName)
            chunk.export(chunkName, format="wav")
            file = chunkName
            r = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio_listened = r.listen(source)
            try:
                rec = r.recognize_google(audio_listened)
                txtf.write(rec+".")
            except sr. UnknownValueError:
                print("I don't recognize your audio")
            except sr.RequestError as e:
                print("could not get the result.check your internet")
    try:
        os.makedirs("chunked")
    except:
        pass

# def main():
#     convert("video.mp4")
#     time.sleep(5)
#     process_audio("video.wav")

# ==== creating main function
def main():
    root = Tk()
    obj = VideoAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
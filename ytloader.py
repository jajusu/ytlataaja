from pytube import YouTube
from sys import argv, exit

def lueAsetukset():
    videoAsetus=""
    audioAsetus=""
    try:
        with open("ytloaderSettings.txt") as tiedosto:
            for rivi in tiedosto:
                rivi = rivi.replace("\n", "")
                osat = rivi.split(",")
                if (osat[0]=="video"):
                    videoAsetus=osat[1]
                if (osat[0]=="audio"):
                    audioAsetus=osat[1]
        print("Videon tallennuspaikka:",videoAsetus)
        print("Äänen tallennuspaikka:",audioAsetus)
        return(videoAsetus,audioAsetus)
    except:
        print("Ongelma asetusten lukemisessa, tallennetaan juureen. Puuttuuko ytloaderSettings.txt?")
        return(videoAsetus,audioAsetus)
        

def lataaTiedostot(videoAsetus,audioAsetus):
    try:
        print("Title:", yt.title)
        video=yt.streams.get_highest_resolution()
        audio=yt.streams.get_audio_only()
        #print("Size: ", round(video.filesize_approx/1024/1024,2), " MB")
        if (asetusParametri=="v" or asetusParametri=="b"):
            video.download(videoAsetus)
            print("Size (video):", round(video.filesize_approx/1024/1024,2), "MB")
        if (asetusParametri=="a" or asetusParametri=="b"):
            audio.download(audioAsetus)
            print("Size (audio):", round(audio.filesize_approx/1024/1024,2), "MB")
        print("Lataus onnistui!")
    except:
        print("Virhe tiedoston latauksessa.")

def muokkaaAsetuksia():
    print("Asetuksien muokkaus")
    kumpiAsetus=""
    while kumpiAsetus!="v" and kumpiAsetus!="a":
        kumpiAsetus=input("Asetetaanko video- vai audiosijainti? Syötä v tai a, 0 poistuu:")
        if (kumpiAsetus=="0"):
            exit(1)
        videoAsetus,audioAsetus=lueAsetukset()
        # print(videoAsetus,audioAsetus)
        if (kumpiAsetus=="v"):
            uusiVideoAsetus=input("Anna videoiden uusi tallennussijainti:")
            tarkistaSijaintiJaTyhjenna(uusiVideoAsetus)
            try:
                with open("ytloaderSettings.txt", "a") as tiedosto:
                    tiedosto.write("video,"+uusiVideoAsetus+"\n")
                    tiedosto.write("audio,"+audioAsetus+"\n")
                print("tallennettu")
            except:
                print("tallennusvirhe")
            exit(1)
        elif (kumpiAsetus=="a"):
            uusiAudioAsetus=input("Anna audion uusi tallennussijainti:")
            tarkistaSijaintiJaTyhjenna(uusiAudioAsetus)
            try:
                with open("ytloaderSettings.txt", "a") as tiedosto:
                    tiedosto.write("video,"+videoAsetus+"\n")
                    tiedosto.write("audio,"+uusiAudioAsetus+"\n")
                print("tallennettu")
            except:
                print("tallennusvirhe")
            exit(1)
    # print(kumpiAsetus)
    
def tarkistaSijaintiJaTyhjenna(sijainti):
    if (sijainti==""):
        print("tyhjä sijainti, ei tallenneta")
        exit(1)
    else:
        open('ytloaderSettings.txt', 'w').close() #asetusten tyhjennys täällä

link=""
try:
    link = argv[1]
except:
    print("          ***************************")
    print("          ***** Youtube-lataaja *****")
    print("          ***************************")
    print(" -Käytä komentoriviltä oikeasta tiedostosijainnista,")
    print("  ytloader.py youtube-linkki parametri.")
    print("  esim. ytloader https://www.youtube.com/watch?v=XXXXXX b")
    print(" -Tiedostosijainnin asetuksiin pääset komennolla: ")
    print("  ytloader.py asetukset")
    print(" -Ilman parametria perässä ladataan video,")
    print("  parametrilla a pelkkä audio ja b:llä molemmat.")
    exit(1)

if (link=="asetukset"):
    muokkaaAsetuksia()
else:
    try:
        yt=YouTube(link)
    except:
        print("vääränlainen linkki.")
        exit(1)

argvPituus=len(argv)
# print(argvPituus)
if (argvPituus==3):
    asetusParametri=argv[2]
elif (argvPituus>3):
    print("liikaa parametrejä")
    exit(1)
else:
    asetusParametri="v"

videoAsetus,audioAsetus=lueAsetukset()
lataaTiedostot(videoAsetus,audioAsetus)

# argv[1] ottaa ensimmäisen komennon talteen komentoriviltä ohjelman suorituksen jälkeen. toimii siis niin, että 
# komentorivillä ytloader.py youtubeurl. jos halutaan pelkkä audio, laitetaan perään a, eli ytloader.py yout a,
# jos molemmat (video ja audio) niin perään b, pelkkä video niin v tai ei parametria.
# esimerkkikomento:
# ytloader.py https://www.youtube.com/shorts/ne6eqVIlS1U b
# tallennustiedoston sijaintia voi muuttaa asetuksissa juuressa olevassa tiedostossa ytloaderSettings.txt
# asetuksia pääsee muokkaamaan myös ytloader.py asetukset
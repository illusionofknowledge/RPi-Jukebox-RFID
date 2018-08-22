#!/bin/bash

# Creates sample folders with streams for 
# * YouTube
# * Podcast
# * Web radio
# inside the shared/audiofolders directory

# ZZZ-Podcast-DLF-Kinderhoerspiele (dir)
# * podcast.txt (file)
# * http://www.kakadu.de/podcast-kinderhoerspiel.3420.de.podcast.xml (content)

AUDIOFOLDERSPATH=`cat ../../settings/Audio_Folders_Path`

mkdir ../../shared/audiofolders/ZZZ-Podcast-DLF-Kinderhoerspiele
echo "http://www.kakadu.de/podcast-kinderhoerspiel.3420.de.podcast.xml" > $AUDIOFOLDERSPATH/ZZZ-Podcast-DLF-Kinderhoerspiele/podcast.txt

# ZZZ-Podcast-Kakadu (dir)
# * podcast.txt (file)
# * http://www.kakadu.de/podcast-kakadu.2730.de.podcast.xml (content)

mkdir ../../shared/audiofolders/ZZZ-Podcast-Kakadu
echo "http://www.kakadu.de/podcast-kakadu.2730.de.podcast.xml" > $AUDIOFOLDERSPATH/ZZZ-Podcast-Kakadu/podcast.txt

# ZZZ-LiveStream-Bayern2 (dir)
# * livestream.txt (file)
# * http://br-br2-nord.cast.addradio.de/br/br2/nord/mp3/56/stream.mp3 (content)

mkdir ../../shared/audiofolders/ZZZ-LiveStream-Bayern2
echo "http://br-br2-nord.cast.addradio.de/br/br2/nord/mp3/56/stream.mp3" > $AUDIOFOLDERSPATH/ZZZ-LiveStream-Bayern2/livestream.txt

# ZZZ-MP3-StartUpSound (dir)
# * startupsound.mp3 (file)

mkdir ../../shared/audiofolders/ZZZ-MP3-StartUpSound
cp ../../misc/sampleconfigs/startupsound.mp3.sample $AUDIOFOLDERSPATH/ZZZ-MP3-StartUpSound/startupsound.mp3

# ZZZ MP3 Whitespace StartUpSound (dir)
# * startupsound.mp3 (file)

mkdir ../../shared/audiofolders/ZZZ\ MP3\ Whitespace\ StartUpSound
cp ../../misc/sampleconfigs/startupsound.mp3.sample $AUDIOFOLDERSPATH/ZZZ\ MP3\ Whitespace\ StartUpSound/startupsound.mp3

# ZZZ-AudioFormatsTest (dir)
# * startupsound.mp3 (file)

mkdir ../../shared/audiofolders/ZZZ-AudioFormatsTest
cp ../../misc/audiofiletype* $AUDIOFOLDERSPATH/ZZZ-AudioFormatsTest/







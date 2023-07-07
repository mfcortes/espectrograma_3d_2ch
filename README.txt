echo "# espectrograma_3d_2ch" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mfcortes/espectrograma_3d_2ch.git
git push -u origin main

deben tener instaladas librerias
Axes3D
librosa
pyaudio
from sklearn.cluster import KMeans


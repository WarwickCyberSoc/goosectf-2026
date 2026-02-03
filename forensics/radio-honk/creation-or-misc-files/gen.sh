sudo apt install ax25-tools
echo "GOOSE-1>GROUND:GooseCTF{H0nk_H0nk_0ff_th3_Gr1d}" > packet.txt
gen_packets -o honk.wav packet.txt
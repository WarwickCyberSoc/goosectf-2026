compile:
	gcc library.c -fstack-protector -Wl,-z,relro,-z,now -Xlinker -rpath="./" -Xlinker -I"./ld-2.27.so" -Xlinker "./libc.so.6"  -o library
clean:
	rm library

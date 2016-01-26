CPPFLAGS=`root-config --cflags` -I/usr/local/root/include
LDFLAGS=`root-config --libs` -lMinuit
TreeReader.exe: TreeReader.cc
        g++ $(CPPFLAGS) $(LDFLAGS) -o $@ $^




DEPS = codepoints.h
OBJ = example.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

example: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

codepoints.h:
	python3 ./libcodepoint.py codepoints.h

.PHONY: clean

clean:
	rm -f *.o
	rm codepoints.h
	rm example

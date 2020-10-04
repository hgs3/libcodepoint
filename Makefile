DEPS = libcodepoint.h
OBJ = example.o

%.o: %.c $(DEPS)
	$(CC) -std=c99 -c -o $@ $< $(CFLAGS)

example: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS)

libcodepoint.h:
	python3 ./libcodepoint.py libcodepoint.h

.PHONY: clean

clean:
	rm -f *.o
	rm libcodepoint.h
	rm example

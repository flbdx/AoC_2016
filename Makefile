CXXFLAGS=-Wall -Wextra
CXXFLAGS+=-O2 -g -std=c++11 -march=native

TARGETS=day_05 day_14 day_16

all: $(TARGETS)

day_05: LDLIBS=-lcrypto
day_14: LDLIBS=-lcrypto

clean:
	rm -f $(TARGETS)

.phony: all clean

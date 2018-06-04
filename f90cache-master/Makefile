srcdir=.


prefix=/usr/local
exec_prefix=${prefix}
bindir=${exec_prefix}/bin
mandir=${prefix}/share/man
INSTALLCMD=/usr/bin/install -c

CC=gcc
CFLAGS=-g -O2 -Wall -W -I.
EXEEXT=

OBJS= f90cache.o mdfour.o hash.o execute.o util.o args.o stats.o \
	cleanup.o snprintf.o

HEADERS = f90cache.h mdfour.h

all: f90cache$(EXEEXT)

f90cache$(EXEEXT): $(OBJS) $(HEADERS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

install: f90cache$(EXEEXT) f90cache.1
	${INSTALLCMD} -d $(DESTDIR)${bindir}
	${INSTALLCMD} -m 755 f90cache$(EXEEXT) $(DESTDIR)${bindir}
	${INSTALLCMD} -d $(DESTDIR)${mandir}/man1
	${INSTALLCMD} -m 644 ${srcdir}/f90cache.1 $(DESTDIR)${mandir}/man1/
	strip $(DESTDIR)${bindir}/f90cache$(EXEEXT)

clean:
	/bin/rm -f $(OBJS) *~ f90cache$(EXEEXT)

distclean: clean
	/bin/rm -f Makefile config.h config.sub config.log build-stamp \
        config.status tags


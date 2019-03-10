#-------------------------------------------------
#
# Project created by QtCreator 2016-04-17T16:23:57
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = NS_shaft
TEMPLATE = app


SOURCES += main.cpp\
        widget.cpp

HEADERS  += widget.h

FORMS    += widget.ui

LIBS += -luser32 -lshell32 -lgdi32

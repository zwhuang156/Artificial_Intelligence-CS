#include "widget.h"
#include <QApplication>
#include <QDesktopWidget>
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Screenshot screenshot;
    screenshot.move(QApplication::desktop()->availableGeometry(&screenshot).topLeft() + QPoint(700, 20));
    screenshot.show();
    return a.exec();
}

#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
#include <QLabel>
#include <QSpinBox>
#include <QCheckBox>
#include <QPushButton>

#include <QPixmap>
#define WINVER 0x0500
#include <Windows.h>
class QCheckBox;
class QGridLayout;
class QGroupBox;
class QHBoxLayout;
class QLabel;
class QPushButton;
class QSpinBox;
class QVBoxLayout;

class Screenshot : public QWidget
{
    Q_OBJECT

public:
    Screenshot();

    int agent_x,agent_y,goal_x,goal_y,initial_x,initial_y;
    int count;
    int state,first;
protected:
    void resizeEvent(QResizeEvent *event) Q_DECL_OVERRIDE;

public slots:
    void newScreenshot();
    void saveScreenshot();
    void shootScreen();
    void updateCheckBox();
    void touch_left();
    void touch_right();
    void touch_stop(int stop_time);
    void start();

private:
    void updateScreenshotLabel();

    QPixmap originalPixmap;

    QLabel *screenshotLabel;
    QSpinBox *delaySpinBox;
    QCheckBox *hideThisWindowCheckBox;
    QPushButton *newScreenshotButton;
    INPUT ip;
};
#endif // WIDGET_H

#include "widget.h"
#include "ui_widget.h"
#include <QVBoxLayout>
#include <QGroupBox>
#include <QTimer>
#include <QApplication>
#include <QtWidgets>
#include <QRect>
#include <QPixmap>
#include <QKeyEvent>
#include <cstdlib>
#include <iostream>
#define WINVER 0x0500
#include <Windows.h>
#include <vector>
#include <math.h>
using namespace std;

struct Tuple  //紀錄階梯與刺的座標
{
    int x;
    int y;  //stair center x , y
    int dis; // distance between head and stair
    Tuple();
    Tuple(int X,int Y):x(X),y(Y){};

};
bool distance_compare(Tuple a, Tuple b)
{
    return a.dis < b.dis;
}


Screenshot::Screenshot():screenshotLabel(new QLabel(this))
{
    screenshotLabel->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
    screenshotLabel->setAlignment(Qt::AlignCenter);

    const QRect screenGeometry = QApplication::desktop()->screenGeometry(this);
    screenshotLabel->setMinimumSize(screenGeometry.width() / 2, screenGeometry.height() / 2);

    QVBoxLayout *mainLayout = new QVBoxLayout(this);
    mainLayout->addWidget(screenshotLabel);

    QHBoxLayout *buttonsLayout = new QHBoxLayout;
    newScreenshotButton = new QPushButton(tr("New Screenshot"), this);
    connect(newScreenshotButton, &QPushButton::clicked, this, &Screenshot::newScreenshot);
    buttonsLayout->addWidget(newScreenshotButton);
    QPushButton *saveScreenshotButton = new QPushButton(tr("Save Screenshot"), this);
    connect(saveScreenshotButton, &QPushButton::clicked, this, &Screenshot::saveScreenshot);
    buttonsLayout->addWidget(saveScreenshotButton);
    QPushButton *quitScreenshotButton = new QPushButton(tr("Start"), this);
    //quitScreenshotButton->setShortcut(Qt::CTRL + Qt::Key_Q);
    connect(quitScreenshotButton, &QPushButton::clicked, this, &Screenshot::start);
    buttonsLayout->addWidget(quitScreenshotButton);
    buttonsLayout->addStretch();
    mainLayout->addLayout(buttonsLayout);

    //shootScreen();

    state=0;
    first=0;
    setWindowTitle(tr("Screenshot"));
    resize(400, 250);

}

void Screenshot::start()
{
    Sleep(200);
    shootScreen();//get a screen shot
}

void Screenshot::touch_left() //按住左鍵
{

    // This structure will be used to create the keyboard
        // input event.
        //INPUT ip;

        // Pause for 5 seconds.
        //Sleep(500);

        // Set up a generic keyboard event.
        ip.type = INPUT_KEYBOARD;
        ip.ki.wScan = 0; // hardware scan code for key
        ip.ki.time = 0;
        ip.ki.dwExtraInfo = 0;

        // Press the "A" key
        ip.ki.wVk = 0x25; // virtual-key code for the "a" key
        ip.ki.dwFlags = 0; // 0 for key press
        SendInput(1,&ip,sizeof(INPUT));
        //Sleep(10);
        //ip.ki.dwFlags = KEYEVENTF_KEYUP; // KEYEVENTF_KEYUP for key release
        //SendInput(1, &ip, sizeof(INPUT));

}
void Screenshot::touch_right() //按住右鍵
{

    // This structure will be used to create the keyboard
        // input event.


        // Pause for 5 seconds.
        //Sleep(500);

        // Set up a generic keyboard event.
        ip.type = INPUT_KEYBOARD;
        ip.ki.wScan = 0; // hardware scan code for key
        ip.ki.time = 0;
        ip.ki.dwExtraInfo = 0;

        // Press the "A" key
        ip.ki.wVk = 0x27; // virtual-key code for the "a" key
        ip.ki.dwFlags = 0; // 0 for key press
        SendInput(1,&ip,sizeof(INPUT));
        //Sleep(50);
        //ip.ki.dwFlags = KEYEVENTF_KEYUP; // KEYEVENTF_KEYUP for key release
        //SendInput(1, &ip, sizeof(INPUT));

}
void Screenshot::touch_stop(int stop_time) //放開按鍵
{

    // This structure will be used to create the keyboard
        // input event.
        //INPUT ip;

        // Pause for 5 seconds.
        //Sleep(500);

        // Set up a generic keyboard event.
        ip.type = INPUT_KEYBOARD;
        ip.ki.wScan = 0; // hardware scan code for key
        ip.ki.time = 0;
        ip.ki.dwExtraInfo = 0;

        // Press the "A" key
        //ip.ki.wVk = 0x27; // virtual-key code for the "a" key
        ip.ki.dwFlags = 0; // 0 for key press
        //SendInput(1,&ip,sizeof(INPUT));

        ip.ki.dwFlags = KEYEVENTF_KEYUP; // KEYEVENTF_KEYUP for key release

        SendInput(1, &ip, sizeof(INPUT));
        Sleep(stop_time);
}
//useless
void Screenshot::resizeEvent(QResizeEvent * /* event */)
{
    QSize scaledSize = originalPixmap.size();
    scaledSize.scale(screenshotLabel->size(), Qt::KeepAspectRatio);
    if (!screenshotLabel->pixmap() || scaledSize != screenshotLabel->pixmap()->size())
        updateScreenshotLabel();
}
//useless
void Screenshot::newScreenshot()
{
    if (hideThisWindowCheckBox->isChecked())
        hide();
    newScreenshotButton->setDisabled(true);

    QTimer::singleShot(delaySpinBox->value() * 1000, this, &Screenshot::shootScreen);
}

void Screenshot::saveScreenshot()
{
    const QString format = "png";
    QString initialPath = QStandardPaths::writableLocation(QStandardPaths::PicturesLocation);
    if (initialPath.isEmpty())
        initialPath = QDir::currentPath();
    initialPath += tr("/untitled.") + format;

    QFileDialog fileDialog(this, tr("Save As"), initialPath);
    fileDialog.setAcceptMode(QFileDialog::AcceptSave);
    fileDialog.setFileMode(QFileDialog::AnyFile);
    fileDialog.setDirectory(initialPath);
    QStringList mimeTypes;
    foreach (const QByteArray &bf, QImageWriter::supportedMimeTypes())
        mimeTypes.append(QLatin1String(bf));
    fileDialog.setMimeTypeFilters(mimeTypes);
    fileDialog.selectMimeTypeFilter("image/" + format);
    fileDialog.setDefaultSuffix(format);
    if (fileDialog.exec() != QDialog::Accepted)
        return;
    const QString fileName = fileDialog.selectedFiles().first();
    if (!originalPixmap.save(fileName)) {
        QMessageBox::warning(this, tr("Save Error"), tr("The image could not be saved to \"%1\".")
                             .arg(QDir::toNativeSeparators(fileName)));
    }
}

void Screenshot::shootScreen()//get a screenshot and AI  //main code here
{
    QScreen *screen = QGuiApplication::primaryScreen();
    if (const QWindow *window = windowHandle())
        screen = window->screen();
    if (!screen)
        return;

    /*if (delaySpinBox->value() != 0)
        QApplication::beep();*/

    originalPixmap = screen->grabWindow(0,25,50,420,420);
    QImage tempImage = originalPixmap.toImage();
//----------------  catch head --------------------------------------------------------
    int agent_x=0,agent_y=0;
    int count=0;
    for ( int row = 65; row < tempImage.height(); ++row ){
        for ( int col = 0; col < tempImage.width(); ++col )
{
            QColor clrCurrent( tempImage.pixel( col, row ) );

            if(clrCurrent.red()>=250&&clrCurrent.green()<=1&&clrCurrent.blue()<=1){
                agent_x=agent_x+col;
                agent_y=agent_y+row;
                count++;
            }
        }
    }
    if(count!=0){
        agent_x=agent_x/count;
        agent_y=agent_y/count;
    }
//----------------------------------------------------------------------------------------
    vector<Tuple> path;
    for ( int row = agent_y; row < tempImage.height()-20; ++row ){
        for ( int col = 0; col < tempImage.width()-100; ++col ){
            QColor clrCurrent( tempImage.pixel( col, row ) );   //階梯
            QColor clrCurrent1( tempImage.pixel( col, row+12 ) );
            QColor clrCurrent2( tempImage.pixel( col+91, row ) );
            QColor clrCurrent3( tempImage.pixel( col+91, row+12 ) );

            if(clrCurrent.red()==204 && clrCurrent.green()==236 && clrCurrent.blue()==255){
                if(clrCurrent1.red()==204 && clrCurrent1.green()==236 && clrCurrent1.blue()==255){
                    if(clrCurrent2.red()==153 && clrCurrent2.green()==153 && clrCurrent2.blue()==255){
                        if(clrCurrent3.red()==153 && clrCurrent3.green()==153 && clrCurrent3.blue()==255){
                            if(abs(col+45-agent_x)<165){
                                if(row>agent_y&&abs(row-agent_y)<30){
                                  initial_x=col+45;
                                  initial_y=row;
                                }
                                else{
                                    QPainter p(&originalPixmap);
                                    p.setPen(Qt::red);
                                    p.drawRect(QRect(col,row,91,12));
                                    p.end();
                                    Tuple temp(col+45,row);
                                    temp.dis=abs(temp.x-agent_x)+abs(temp.y-agent_y);
                                    path.push_back(temp);
                                }
                            }
                       }
                  }
              }
            }
            QColor clrCurrent4( tempImage.pixel( col, row ) );   //刺
            QColor clrCurrent5( tempImage.pixel( col, row+11 ) );
            QColor clrCurrent6( tempImage.pixel( col+91, row+11 ) );
            QColor clrCurrent7( tempImage.pixel( col+91, row ) );

            if(clrCurrent4.red()==192&&clrCurrent4.green()==192&&clrCurrent4.blue()==192)
            {
              if(clrCurrent5.red()==178&&clrCurrent5.green()==178&&clrCurrent5.blue()==178)
              {
                  if(clrCurrent6.red()==153&&clrCurrent6.green()==153&&clrCurrent6.blue()==153)
                  {
                      if(clrCurrent7.red()==160&&clrCurrent7.green()==160&&clrCurrent7.blue()==164)
                      {
                          if(abs(col+45-agent_x)<165)
                          {
                              if(row>agent_y&&abs(row-agent_y)<30)
                              {
                                  initial_x=col+45;
                                  initial_y=row;


                              }


                           }
                          QPainter p(&originalPixmap);
                          //p.setBrush(Qt::blue);
                          p.setBrush(QBrush(Qt::blue, Qt::DiagCrossPattern));
                          //p.setPen(Qt::blue);
                          p.drawRect(QRect(col,row,91,12));
                          p.end();
                          //updateScreenshotLabel();
                          //cout<<col<<" "<<row<<endl;
                      }
                  }
              }
            }

        }
    }
/*
    QPainter temp(&originalPixmap);
    temp.setBrush(QBrush(Qt::white, Qt::DiagCrossPattern));
    temp.drawRect(QRect(initial_x-45,initial_y,91,12));
    temp.end();
    cout<<"initial_x:"<<initial_x<<" "<<"initial_y:"<<initial_y<<endl;
    cout<<agent_x<<" "<<agent_y<<endl;
    if(path.size()>=0)
    {

        if(state==0&&path.size()>0)
        {
            sort(path.begin(),path.end(),distance_compare);
            cout<<state<<endl;
            QPainter p(&originalPixmap);
            //p.setBrush(Qt::blue);
            p.setBrush(QBrush(Qt::red, Qt::DiagCrossPattern));
            //p.setPen(Qt::blue);
            p.drawRect(QRect(path[0].x-45,path[0].y,91,12));
            p.end();
            if(path.size()>=1)
            {

                if(path[0].x<=initial_x&&initial_x<90)
                {
                    touch_right();
                    if(agent_x>initial_x+60)
                    {
                        state=1;
                        touch_stop(10);
                        goal_x=path[0].x;
                        goal_y=path[0].y;
                    }

                }
                else if(path[0].x>=initial_x&&initial_x>320){
                    touch_left();
                    if(agent_x<initial_x-60){
                        state=1;
                        touch_stop(10);
                        goal_x=path[0].x;
                        goal_y=path[0].y;

                    }

                }
                else if(path[0].x>=initial_x)
                {
                    touch_right();
                    if(agent_x>initial_x+60)
                    {
                        state=1;
                        //initial_x=100;
                        //initial_y=50;
                        if(path[0].x-45>initial_x+45)
                        {

                        }
                        else
                        {
                            touch_stop(10);
                        }
                        goal_x=path[0].x;
                        goal_y=path[0].y;

                    }

                }
                else
                {
                    touch_left();
                    if(agent_x<initial_x-60)
                    {
                        state=1;
                        //initial_x=100;
                        //initial_y=50;
                        if(path[0].x+45<initial_x-45)
                        {

                        }
                        else
                        {
                            touch_stop(10);
                        }
                        goal_x=path[0].x;
                        goal_y=path[0].y;

                    }

                }
            }
        }
        else if(state==1)
        {
            cout<<state<<endl;
            QPainter p(&originalPixmap);
            //p.setBrush(Qt::blue);
            p.setBrush(QBrush(Qt::red, Qt::DiagCrossPattern));
            //p.setPen(Qt::blue);
            p.drawRect(QRect(goal_x-45,goal_y,91,12));
            p.end();
            if(initial_x-57<agent_x&&initial_x+57>agent_x&&abs(initial_y-agent_y)<30&&initial_y>agent_y)
            {
                cout<<"arrive"<<endl;
                touch_stop(10);
                state=0;
            }
            else if(agent_y>goal_y)
            {
                state=0;
                touch_stop(10);
            }
            else
            {
                if(goal_x-45>=initial_x+45)
                {

                    if(goal_x-45>agent_x)
                    {
                        //touch_right();

                    }
                    else
                    {
                        touch_stop(10);
                    }
                }
                else if(goal_x+45<=initial_x-45)
                {
                    if(goal_x+45<agent_x)
                    {
                        //touch_left();
                    }
                    else
                    {
                        touch_stop(10);
                    }
                }
                else
                {
                    if(goal_x+45<agent_x&&agent_x>goal_x-45)
                    {
                        touch_left();
                    }
                    else if(goal_x-45>agent_x&&goal_x+45>agent_x)
                    {
                        touch_right();
                    }
                    else
                    {
                        touch_stop(10);
                    }
                }
            }
        }
    }

*/

    updateScreenshotLabel();
      QPainter p(&originalPixmap);
      p.setPen(Qt::red);
      p.drawRect(QRect(agent_x-5,agent_y-5,10,10));
      p.end();
      updateScreenshotLabel();


    path.clear();
    QTimer::singleShot(30, this, &Screenshot::shootScreen);

}
//useless
void Screenshot::updateCheckBox()
{
    if (delaySpinBox->value() == 0) {
        hideThisWindowCheckBox->setDisabled(true);
        hideThisWindowCheckBox->setChecked(false);
    } else {
        hideThisWindowCheckBox->setDisabled(false);
    }
}

void Screenshot::updateScreenshotLabel()
{
    screenshotLabel->setPixmap(originalPixmap.scaled(screenshotLabel->size(),Qt::KeepAspectRatio,Qt::SmoothTransformation));
}

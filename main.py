import cv2

temp=0
img=cv2.imread('test.png', 1)
##马赛克
def do_mosaic(frame, x, y, w, h, neighbor=9):
    """
    马赛克的实现原理是把图像上某个像素点一定范围邻域内的所有点用邻域内左上像素点的颜色代替，这样可以模糊细节，但是可以保留大体的轮廓。
    :param frame: opencv frame
    :param int x :  马赛克左顶点
    :param int y:  马赛克右顶点
    :param int w:  马赛克宽
    :param int h:  马赛克高
    :param int neighbor:  马赛克每一块的宽
    """
    fh, fw = frame.shape[0], frame.shape[1]
    if (y + h > fh) or (x + w > fw):
        return
    for i in range(0, h - neighbor, neighbor):  # 关键点0 减去neightbour 防止溢出
        for j in range(0, w - neighbor, neighbor):
            color = frame[i + y][j + x].tolist()  # 关键点1 tolist
            left_up = (j+x, i+y)
            right_down = (j+x + neighbor - 1, i+y + neighbor - 1)  # 关键点2 减去一个像素
            cv2.rectangle(frame, left_up, right_down, color, -1)
            #把一大块的颜色都指定成color--也就是我们之前取的左上角的颜色
    return frame

def on_mouse(event, x, y, flags, param):
    global img,point1, point2, g_rect
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击,则在原图打点
        print("1-EVENT_LBUTTONDOWN")
        point1 = (x, y)
        cv2.circle(img2, point1, 10, (0, 255, 0), 5)
        cv2.imshow('img', img2)

    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳，画框
        print("2-EVENT_FLAG_LBUTTON")
        cv2.rectangle(img2, point1, (x, y), (255, 0, 0), thickness=2)
        cv2.imshow('img', img2)

    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放，显示
        print("3-EVENT_LBUTTONUP")
        point2 = (x, y)
        #cv2.rectangle(img2, point1, point2, (0, 0, 255), thickness=2)
        global temp
        temp=img.copy()
        now=do_mosaic(img, point1[0],point1[1], point2[0]-point1[0], point2[1]-point1[1])
        cv2.imshow('img',now)

cv2.namedWindow("img",0)
cv2.resizeWindow("img",640, 480)
while True:
    cv2.setMouseCallback('img', on_mouse)
    # cv2.startWindowThread()  # 加在这个位置
    cv2.imshow('img', img)
    key = cv2.waitKey(0)
    if key ==27: # 按esc退出
        break
    if key == 8:
        img=temp    #按回退键为撤销上一步马赛克操作
        print('back')
        cv2.imshow('img',img)
    if key==13:     #回车键保存
        cv2.imwrite('temp.jpg', img)
        print('保存成功')
        break
cv2.destroyAllWindows()
#do_mosaic(im, 219, 61, 460 - 219, 412 - 61)
cv2.waitKey(0)

import cv2
from tkinter.filedialog import *
temp=0
pic_path = askopenfilename(title="选择图片")
# 取得文件路径
img=cv2.imread(pic_path, 1)
##马赛克
def do_mosaic(img,x,y,w,h,neighbor=20):  # neighbor is the masaic degree
    img_height = img.shape[0]
    img_width = img.shape[1]
    for i in range(x,x+w,neighbor):
        for j in range(y,y+h,neighbor):
            color=img[j+1][i+1].tolist() #image matrix [height][widith]
            cv2.rectangle(img,(i,j),(i+neighbor,j+neighbor),color,-1)
    return img

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
    key = cv2.waitKey(0)#监听！！！
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

# Adventure Game
## Dự án Game Platform kết hợp nhận dạng xử lý ảnh với OpenCV
1. Xây dựng Game Platform.
2. Điều khiển game bằng bàn phím (EASY MODE).
2. Điều khiển game bằng nhận dạng cử động bàn tay (HARD MODE).
3. Đăng ký, đăng nhập bằng nhận diện khuôn mặt.
4. Xây dựng cơ chế tự thiết kế màn chơi cho người chơi.
5. Xây dựng chức năng history và ranking.
## Cài đặt

1. Cài đặt Anaconda https://www.anaconda.com/
2. Clone source
```console
$ git clone https://github.com/lequanphat/Adventure-Game.git
```


3. Tạo môi trường python 3.8
```console
$ conda create --name myenv python=3.8
```
4. Kích hoạt môi trường
```console
$ conda activate myenv
```
5. Cài đặt các gói cần thiết
```console
$ conda install pygame
$ conda install opencv-python
$ conda install mediapipe
```
6. Run
```console
$ python main.py
```

## Hướng dẫn khắc phục lỗi cài đặt dlib
Python 3.7
```console
$ conda install library/dlib-19.22.99-cp37-cp37m-win_amd64.whl
```
Python 3.8
```console
$ conda install library/dlib-19.22.99-cp38-cp38-win_amd64.whl
```
Python 3.9
```console
$ conda install library/dlib-19.22.99-cp39-cp39-win_amd64.whl
```
## Demo
### Tự động đăng nhập bằng nhận diện khuôn mặt 
![GitHub Logo](/demo/1.jpg)
### Màn hình trò chơi 
![GitHub Logo](/demo/2.jpg)
### Màn hình chỉnh sửa màn chơi
![GitHub Logo](/demo/3.jpg)
### Điều khiển bằng nhận dạng chuyển động bàn tay
![GitHub Logo](/demo/4.jpg)
### Đăng ký nhận diện khuôn mặt
![GitHub Logo](/demo/5.jpg)
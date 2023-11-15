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
$ conda install numpy
$ conda install pandas
$ conda install cmake
```
6. Run
```console
$ python main.py
```

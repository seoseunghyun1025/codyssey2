import cv2
import csv
import os

# 1. 카메라 영상 출력 함수
def show_camera_output():
    cap = cv2.VideoCapture(0)  # 첫 번째 카메라 사용
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    # 카메라 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("카메라에서 프레임을 읽을 수 없습니다.")
            break

        # 실시간 영상 출력
        cv2.imshow('Camera Output', frame)

        # 33ms 대기 (키 입력 대기)
        key = cv2.waitKey(33)

        # 'q' 키를 누르면 종료
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 2. 이미지 출력 함수
def show_image(image_path):
    img = cv2.imread(image_path)  # 이미지를 읽음
    if img is None:
        print(f"이미지 파일을 열 수 없습니다: {image_path}")
        return
    
    cv2.imshow('Image', img)
    
    # 키 입력 대기 (무한 대기, 'q' 키를 누르면 종료)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 3. 동영상 출력 함수
def show_video(video_path):
    cap = cv2.VideoCapture(video_path)  # 동영상 파일 열기
    if not cap.isOpened():
        print(f"동영상을 열 수 없습니다: {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("동영상이 끝났습니다.")
            break

        cv2.imshow('Video Output', frame)

        # 33ms 대기
        key = cv2.waitKey(33)

        # 'q' 키를 누르면 종료
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 함수 실행 예시
show_camera_output()  # 카메라 영상 출력
show_image("sample_image.jpg")  # 이미지 출력
show_video("sample_video.mp4")  # 동영상 출력

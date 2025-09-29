import cv2
import csv
import os  # os 모듈을 임포트 해야 합니다.

# 방명록 저장 함수
def save_to_csv(name, message):
    file_exists = os.path.exists(CSV_FILE_PATH)  # os 모듈을 사용하여 파일이 있는지 확인
    with open(CSV_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Name", "Message"])  # 헤더 추가
        writer.writerow([name, message])  # 데이터 추가

# 방명록 조회 함수
def get_guestbook_entries():
    if not os.path.exists(CSV_FILE_PATH):  # os 모듈을 사용하여 파일이 있는지 확인
        return []
    with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        entries = list(reader)
        return entries[1:]  # 헤더 제외

# 방명록 데이터 입력 함수
def create_entry():
    print("=== 방명록 ===")
    name = input("이름을 입력하세요: ")
    message = input("메시지를 입력하세요: ")
    save_to_csv(name, message)
    print("방명록에 저장되었습니다.")

# 방명록 데이터 조회 함수
def read_guestbook():
    print("=== 방명록 조회 ===")
    entries = get_guestbook_entries()
    if not entries:
        print("방명록에 아무런 데이터가 없습니다.")
        return
    for entry in entries:
        print(f"이름: {entry[0]}, 메시지: {entry[1]}")

# 카메라 영상 출력 함수 (이 부분을 추가하세요)
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

# 이미지 출력 함수
def show_image(image_path):
    img = cv2.imread(image_path)  # 이미지를 읽음
    if img is None:
        print(f"이미지 파일을 열 수 없습니다: {image_path}")
        return
    
    cv2.imshow('Image', img)
    
    # 키 입력 대기 (무한 대기, 'q' 키를 누르면 종료)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 동영상 출력 함수
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

# 메인 실행 함수
def main():
    while True:
        print("\n1. 방명록 입력")
        print("2. 방명록 조회")
        print("3. 카메라 영상 출력")
        print("4. 이미지 출력")
        print("5. 동영상 출력")
        print("6. 종료")
        
        choice = input("원하는 작업을 선택하세요: ")
        
        if choice == '1':
            create_entry()  # 방명록 입력
        elif choice == '2':
            read_guestbook()  # 방명록 조회
        elif choice == '3':
            show_camera_output()  # 카메라 출력
        elif choice == '4':
            image_path = input("이미지 파일 경로를 입력하세요: ")
            show_image(image_path)  # 이미지 출력
        elif choice == '5':
            video_path = input("동영상 파일 경로를 입력하세요: ")
            show_video(video_path)  # 동영상 출력
        elif choice == '6':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 시도하세요.")

# 프로그램 시작
if __name__ == "__main__":
    CSV_FILE_PATH = 'guestbook.csv'  # CSV 파일 경로
    main()

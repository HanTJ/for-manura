import cv2
import subprocess
import time
from datetime import datetime
import os
import shutil

ADB = "C:\\Users\\cruel\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"

"""
광고 자동 클릭 메크로 마눌님을 위하여!
1. 시작버튼 활성화 체크 - 반복 -> 클릭
2. 광고 종료 버튼 서치  - 반복 -> 클릭
3. 1로 가서 반복!
"""

# 스크린샷 찍기
def take_screenshot():
    #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #screenshot_filename = f"screenshot_{timestamp}.png"
    screenshot_filename = "screenshot.png"
    subprocess.run([ADB, "exec-out", "screencap", "-p", f"/sdcard/{screenshot_filename}"])
    subprocess.run([ADB, "pull", f"/sdcard/{screenshot_filename}", "."])
    return screenshot_filename

# 이미지 분석
def find_x_shape(screenshot_filename):
    image = cv2.imread(screenshot_filename)
    template = cv2.imread("x_shape.png", 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        return max_loc
    return None


# 이미지 분석 및 사각형 표시
def find_x_shape_and_draw_rectangle(screenshot_filename):
    image = cv2.imread(screenshot_filename)
    template = cv2.imread("./shapes/x_shape.png", 0)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        top_left = max_loc
        bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        marked_filename = f"marked_{screenshot_filename}"
        cv2.imwrite(marked_filename, image)
        return max_loc, marked_filename
    return None, None

# 이미지 분석 및 사각형 표시
def find_x_shapes_and_draw_rectangles(screenshot_filename, template_files):
    image = cv2.imread(screenshot_filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    found_locations = []

    for template_file in template_files:
        template = cv2.imread(template_file, 0)
        result = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        threshold = 0.8
        if max_val >= threshold:
            top_left = max_loc
            bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
            found_locations.append((top_left[0] + template.shape[1] // 2, top_left[1] + template.shape[0] // 2))

    if found_locations:
        marked_filename = f"marked_{screenshot_filename}"
        cv2.imwrite(marked_filename, image)
        return found_locations, marked_filename
    return None, None

# 클릭 이벤트 발생
def click_event(locations):
    for location in locations:
        x, y = location
        subprocess.run([ADB, "shell", "input", "tap", str(x), str(y)])

# 이미지 백업이동
def backup_images():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_screenshot_filename = f"screenshot_{timestamp}.png"
    new_marked_filename = f"marked_screenshot_{timestamp}.png"
    old_screenshot_filename = "screenshot.png"
    old_marked_filename= "marked_screenshot.png"
    
    if(os.path.isfile(old_screenshot_filename)):
        shutil.move(old_screenshot_filename,os.path.join('./capture',new_screenshot_filename))
    if(os.path.isfile(old_marked_filename)):
        shutil.move(old_marked_filename,os.path.join('./capture',new_marked_filename))

# 메인 함수
def main():
    screenshot_filename = take_screenshot()
    #location = find_x_shape(screenshot_filename)
    #location, marked_filename = find_x_shape_and_draw_rectangle(screenshot_filename)
    locations, marked_filename = find_x_shapes_and_draw_rectangles(screenshot_filename, template_files)
    if locations:
        click_event(locations)
        print(f"X 모양을 찾았습니다. {marked_filename} 파일에 사각형으로 표시되었습니다.")
    else:
        print("X 모양을 찾을 수 없습니다.")
    backup_images()

if __name__ == "__main__":
    template_files = ["./shapes/"+f for f in os.listdir('./shapes') if f.startswith('x_shape') and f.endswith('.png')]
    while True:
        main()
        time.sleep(30)

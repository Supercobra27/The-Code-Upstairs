import cv2 as cv
import numpy as np

def region_of_interest(image):
    height, width = image.shape[:2]
    mask = np.zeros_like(image)
    
    # Define a triangular region for the lane
    polygon = np.array([[
        (width * 0.1, height),
        (width * 0.9, height),
        (width * 0.5, height * 0.6)
    ]], np.int32)
    
    cv.fillPoly(mask, polygon, 255)
    masked_image = cv.bitwise_and(image, mask)
    return masked_image

def detect_edges(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150)
    return edges

def draw_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return line_image

def lane_detection(frame):
    edges = detect_edges(frame)
    roi = region_of_interest(edges)
    
    # Hough Transform to detect lane lines
    lines = cv.HoughLinesP(roi, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=150)
    line_image = draw_lines(frame, lines)
    
    # Overlay the detected lines on the original frame
    result = cv.addWeighted(frame, 0.8, line_image, 1, 1)
    return result

if __name__ == "__main__":
    cap = cv.VideoCapture("road_video.mp4")  # Change to 0 for webcam
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = lane_detection(frame)
        cv.imshow("Lane Detection", processed_frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv.destroyAllWindows()

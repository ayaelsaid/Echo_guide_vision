import cv2
import PIL.Image

class CameraHandler:
    """Manages camera operations for capturing images."""
    def __init__(self):
        self.image_capture = None

    def start_camera(self):
        """Starts the camera."""
        if self.image_capture is None or not self.image_capture.isOpened():
            self.image_capture = cv2.VideoCapture(0)
            if not self.image_capture.isOpened():
                raise Exception("Camera not available. Ensure it's connected and not in use by another application.")
            print("📸 Camera ready.")
        return True

    def take_capture(self):
        """Captures an image and returns it as a PIL Image."""
        if self.image_capture is None or not self.image_capture.isOpened():
            print("Camera is not running. Please start the camera first.")
            return None

        ret, frame = self.image_capture.read()
        if not ret:
            print("Failed to capture frame from camera.")
            return None

        cv2.imshow("Camera", frame)
        cv2.waitKey(1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        pil_img = PIL.Image.fromarray(frame_rgb)
        pil_img = pil_img.resize((200, 200))
        print("✅ Image captured successfully.")
        return pil_img

    def stop_camera(self):
        """Stops the camera and releases resources."""
        if self.image_capture and self.image_capture.isOpened():
            self.image_capture.release()
            cv2.destroyAllWindows()
            print("🚫 Camera closed.")
        self.image_capture = None
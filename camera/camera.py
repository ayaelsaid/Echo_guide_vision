import cv2
import PIL.Image

class CameraHandler:
    """
    Manages camera operations for capturing images using OpenCV.

    This class provides methods to:
    - Start the camera
    - Capture a frame and convert it to a PIL image
    - Stop and release the camera resources
    """

    def __init__(self):
        """
        Initializes the CameraHandler instance.

        Attributes:
            image_capture (cv2.VideoCapture): The OpenCV video capture object.
        """
        self.image_capture = None

    def start_camera(self):
        """
        Starts the camera if it's not already running.

        Returns:
            bool: True if the camera starts successfully.

        Raises:
            Exception: If the camera cannot be accessed or is in use.
        """
        if self.image_capture is None or not self.image_capture.isOpened():
            self.image_capture = cv2.VideoCapture(0)
            if not self.image_capture.isOpened():
                raise Exception("Camera not available. Ensure it's connected and not in use by another application.")
            print("📸 Camera ready.")
        return True

    def take_capture(self):
        """
        Captures a single frame from the camera and returns it as a resized PIL image.

        Returns:
            PIL.Image.Image or None: The captured image in RGB format resized to 200x200,
                                     or None if capture fails or camera is not running.

        Side Effects:
            Displays the captured frame in a window using OpenCV.
        """
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
        print("Image captured successfully.")
        return pil_img

    def stop_camera(self):
        """
        Stops the camera and releases associated resources.

        Side Effects:
            Closes any OpenCV windows and releases the video capture object.
        """
        if self.image_capture and self.image_capture.isOpened():
            self.image_capture.release()
            cv2.destroyAllWindows()
            print("🚫 Camera closed.")
        self.image_capture = None
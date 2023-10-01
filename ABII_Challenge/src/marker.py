import cv2
import numpy as np
import math
class MarkerDetector:
    def __init__(self, init_frame: np.ndarray, target_marker_width: float = 0.10, nav_marker_width: float = 0.27) -> None:
        self.target_marker_width = target_marker_width
        self.nav_marker_width = nav_marker_width
        self.height, self.width = init_frame.shape[:2]
        self.dict_aruco_target = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        self.dict_aruco_nav = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.loaded = False
        self.matrix = None
        self.distortion = None
        self.new_camera_matrix = None
        self.roi = None
        self.x_offset = self.y_offset = None
        self.load_calibration()

    def load_calibration(self):
        if not self.loaded:
            with np.load("calibration_files/camcalib.npz") as X:
                self.matrix = X["mtx"]
                self.distortion = X["dist"]
            self.new_camera_matrix, self.roi = cv2.getOptimalNewCameraMatrix(
                self.matrix,
                self.distortion,
                (self.width, self.height),
                1,
                (self.width, self.height),
            )
            self.x_offset, self.y_offset, self.width, self.height = self.roi
            self.loaded = True

    def detect_markers(self, gray_frame: np.ndarray, marker_dict: dict):
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray_frame, marker_dict, parameters=self.parameters
        )
        return np.array(corners), ids

    def process_frame(self, frame: np.ndarray):
        undistorted_frame = cv2.undistort(
            frame, self.matrix, self.distortion, None, self.new_camera_matrix
        )
        gray_frame = cv2.cvtColor(undistorted_frame, cv2.COLOR_RGB2GRAY)
        target_corners, target_ids = self.detect_markers(
            gray_frame, self.dict_aruco_target
        )
        nav_corners, nav_ids = self.detect_markers(gray_frame, self.dict_aruco_nav)
        self.draw_markers(frame, target_corners, target_ids, "Target")
        self.draw_markers(frame, nav_corners, nav_ids, "Navigation")
        target_info = self.estimate_pose_and_draw_axes(frame, target_corners, target_ids, "Target")
        nav_info = self.estimate_pose_and_draw_axes(frame, nav_corners, nav_ids, "Navigation")
        return frame, {'Target': target_info, 'Navigation': nav_info}

    def draw_markers(self, frame: np.ndarray, corners: np.ndarray, ids: list, marker_class: str = ""):
        if ids is None or marker_class is None:
            return
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        for i, id_value in enumerate(ids):
            marker_label = f"{marker_class} ID {id_value}"
            x, y = int(corners[i][0][:, 0].mean()), int(corners[i][0][:, 1].mean())
            cv2.putText(frame, marker_label, (x, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    def estimate_pose_and_draw_axes(self, frame: np.ndarray, corners: np.array, ids: list, marker_type: str):
        marker_info = []  # Define this at the beginning of your method

        if ids is None:
            return

        # Determine the marker width based on the type of marker
        marker_width = self.target_marker_width if marker_type == "Target" else self.nav_marker_width

        rotations_vecs, translation_vecs, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners, marker_width, self.matrix, self.distortion
        )

        for i, (corner, rot_vec, tran_vec) in enumerate(zip(corners, rotations_vecs, translation_vecs)):
            aruco_id = ids[i][0]
            z_string = f"{tran_vec[0][2]:.2f}"
            x_offset = corner[0][:, 0].mean() - self.width / 2
            marker_info.append({
                'id': int(aruco_id),
                'distance': float(z_string),
                'x_offset': float(x_offset)
            })

        return marker_info
    
def calculate_actual_distance_and_angle(pixel_offset, z_distance, focal_length):
    # Calculate the actual lateral offset (X) in meters
    X = (pixel_offset * z_distance) / focal_length
    
    # Calculate the angle (theta) in radians
    theta_rad = math.atan(X / z_distance)
    
    # Convert the angle to degrees if needed
    theta_deg = math.degrees(theta_rad)
    
    # Calculate the actual distance (D) in meters
    D = math.sqrt(X**2 + z_distance**2)
    
    return D, theta_deg
# Initialize the camera
cap = cv2.VideoCapture(0)

# Get an initial frame to initialize the MarkerDetector
ret, init_frame = cap.read()
if not ret:
    print("Failed to get the initial frame.")
    exit()

# Initialize the marker detector
marker_detector = MarkerDetector(init_frame, target_marker_width=0.10, nav_marker_width=0.27)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture the frame. Exiting...")
        break

    processed_frame, marker_data = marker_detector.process_frame(frame)
    
    if marker_data['Target'] is not None:  # Check if not None before iterating
        for info in marker_data['Target']:
            print(f"Target ID: {info['id']}, Distance: {info['distance']}, X Offset: {info['x_offset']}")
            print(calculate_actual_distance_and_angle(info['x_offset'], info['distance'], 50))
            
    if marker_data['Navigation'] is not None:  # Check if not None before iterating
        for info in marker_data['Navigation']:
            print(f"Navigation ID: {info['id']}, Distance: {info['distance']}, X Offset: {info['x_offset']}")
            
    cv2.imshow("ArUco Markers", processed_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np


def open_camera() -> cv2.VideoCapture:
    """
    Try common camera backends on Windows and return
    the first one that successfully captures a frame.
    """
    # On many Windows laptops, DSHOW is more stable than MSMF.
    backend_candidates = [
        ("DSHOW", cv2.CAP_DSHOW),
        ("MSMF", cv2.CAP_MSMF),
        ("ANY", cv2.CAP_ANY),
    ]

    for name, backend in backend_candidates:
        cap = cv2.VideoCapture(0, backend)
        if not cap.isOpened():
            cap.release()
            continue

        ok, frame = cap.read()
        if ok and frame is not None and frame.size > 0:
            print(f"Camera opened with backend: {name}")
            return cap

        cap.release()

    raise RuntimeError(
        "Could not access laptop camera. Close other camera apps (Zoom/Teams), "
        "then try again."
    )


def enhance_frame(frame: np.ndarray) -> np.ndarray:
    """
    Real-time enhancement:
    1) Improve local contrast with CLAHE (helps reduce hazy look)
    2) Mild denoise + detail boost for clearer output
    """
    # Convert to LAB so we can enhance brightness channel only
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)

    lab_enhanced = cv2.merge((l_enhanced, a, b))
    enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

    # Slight denoise to reduce grain after contrast enhancement
    denoised = cv2.bilateralFilter(enhanced, d=5, sigmaColor=40, sigmaSpace=40)

    # Mild sharpening for clearer edges
    blurred = cv2.GaussianBlur(denoised, (0, 0), sigmaX=1.0)
    sharpened = cv2.addWeighted(denoised, 1.35, blurred, -0.35, 0)

    return sharpened


def draw_face_circle(frame: np.ndarray, face_cascade: cv2.CascadeClassifier) -> np.ndarray:
    """Detect faces and draw a circle around each detected face."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=6,
        minSize=(60, 60),
    )

    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 2
        radius = int(max(w, h) * 0.6)
        cv2.circle(frame, (cx, cy), radius, (0, 255, 0), 3)

    return frame


def main() -> None:
    face_xml = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(face_xml)

    if face_cascade.empty():
        raise RuntimeError("Could not load face detector cascade file.")

    cap = open_camera()

    # Optional camera settings (safe defaults)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "Live Camera - Enhanced + Face Circle"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    print("Press 'q' or ESC to quit.")
    while True:
        try:
            ok, frame = cap.read()
        except cv2.error as err:
            print(f"Camera read error: {err}")
            break

        # Guard against malformed frames from flaky camera backends.
        if (not ok) or (frame is None) or (frame.size == 0):
            print("Invalid frame received from camera. Stopping safely.")
            break

        enhanced = enhance_frame(frame)
        output = draw_face_circle(enhanced, face_cascade)

        cv2.imshow(window_name, output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

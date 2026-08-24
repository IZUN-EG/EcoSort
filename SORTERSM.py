import tensorflow as tf
import numpy as np
import cv2
import time

MODEL_PATH = r"modeloDEFF\model.savedmodel"
class_names = ["Plastico", "Metal", "Papel", "NULL"]
CHANGE_THRESHOLD = 10.0
ROI_WIDTH = 300
ROI_HEIGHT = 300
STABILIZATION_TIME = 2.0
NUM_PREDICTIONS = 7
PREDICTION_INTERVAL = 0.15
CAMERA_INDEX = 1

def detectar_residuo():
    print("Cargando modelo...")
    model = tf.saved_model.load(MODEL_PATH)
    predict = model.signatures["serving_default"]
    print("Modelo cargado correctamente.")
    print("Abriendo cámara...")
    cap = cv2.VideoCapture(CAMERA_INDEX)

    if not cap.isOpened():
        print("ERROR: no se pudo abrir la WebCam.")
        return

    ret, frame = cap.read()
    if not ret:
        print("ERROR: no se pudo obtener el frame inicial.")
        cap.release()
        return

    height, width, _ = frame.shape
    x1 = (width - ROI_WIDTH) // 2
    y1 = (height - ROI_HEIGHT) // 2
    x2 = x1 + ROI_WIDTH
    y2 = y1 + ROI_HEIGHT
    reference_roi = frame[y1:y2, x1:x2].copy()

    print("\n======================================")
    print("       ECOSORT - RECONOCIMIENTO")
    print("======================================")
    print("Sistema iniciado.")
    print("Esperando residuo...\n")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: no se pudo obtener frame.")
                continue

            current_roi = frame[y1:y2, x1:x2]
            difference = cv2.absdiff(current_roi, reference_roi)
            gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
            _, threshold = cv2.threshold(gray_difference, 30, 255, cv2.THRESH_BINARY)
            changed_pixels = cv2.countNonZero(threshold)
            total_pixels = threshold.size
            change_percentage = (changed_pixels / total_pixels) * 100
            residue_detected = change_percentage > CHANGE_THRESHOLD

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if residue_detected:
                print("\nResiduo detectado.")
                print("Esperando 2 segundos para estabilización...")

                cv2.putText(frame, "RESIDUO DETECTADO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                cv2.putText(frame, "ESTABILIZANDO...", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                cv2.imshow("EcoSort", frame)
                cv2.waitKey(1)
                time.sleep(STABILIZATION_TIME)

                predictions = []

                for i in range(NUM_PREDICTIONS):
                    ret, prediction_frame = cap.read()
                    if not ret:
                        print("ERROR: no se pudo capturar frame.")
                        continue

                    image = cv2.resize(prediction_frame, (224, 224))
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    image = image.astype(np.float32) / 255.0
                    image = np.expand_dims(image, axis=0)

                    prediction = predict(tf.constant(image))
                    output = list(prediction.values())[0].numpy()[0]
                    class_index = np.argmax(output)
                    confidence = output[class_index]
                    class_name = class_names[class_index]
                    confidence_percentage = confidence * 100
                    predictions.append((class_name, confidence_percentage))

                    cv2.rectangle(prediction_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(prediction_frame, f"{class_name}: {confidence_percentage:.1f}%", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(prediction_frame, f"Prediccion {i + 1}/{NUM_PREDICTIONS}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow("EcoSort", prediction_frame)
                    cv2.waitKey(1)
                    time.sleep(PREDICTION_INTERVAL)

                if not predictions:
                    print("No se obtuvieron predicciones.")
                    continue

                class_counts = {}
                for class_name, _ in predictions:
                    class_counts[class_name] = class_counts.get(class_name, 0) + 1

                final_class = max(class_counts, key=class_counts.get)
                winning_confidences = [confidence for class_name, confidence in predictions if class_name == final_class]
                final_confidence = sum(winning_confidences) / len(winning_confidences)
                votes = class_counts[final_class]
                vote_percentage = (votes / len(predictions)) * 100

                print("\n======================================")
                print("       RESULTADO ESTADÍSTICO")
                print("======================================")
                print(f"Clase: {final_class}")
                print(f"Confianza promedio: {final_confidence:.1f}%")
                print(f"Votos: {votes}/{len(predictions)}")
                print(f"Consistencia: {vote_percentage:.1f}%")
                print("======================================")

                cv2.putText(prediction_frame, f"{final_class}: {final_confidence:.1f}%", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.putText(prediction_frame, f"Consistencia: {vote_percentage:.1f}%", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("EcoSort", prediction_frame)
                cv2.waitKey(1)

                yield final_class, final_confidence

            else:
                cv2.putText(frame, "ESPERANDO RESIDUO", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.putText(frame, f"Cambio: {change_percentage:.1f}%", (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.imshow("EcoSort", frame)

            if cv2.waitKey(1) == ord("q"):
                print("\nCerrando reconocimiento...")
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Sistema de reconocimiento cerrado.")
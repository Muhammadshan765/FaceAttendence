import base64
import numpy as np
import cv2
import json

def get_face_encoding(image_base64):
    try:
        from deepface import DeepFace
    except ImportError:
        return None, "DeepFace library is not installed. Run: pip install deepface"

    try:
        # Decode the base64 string
        format, imgstr = image_base64.split(';base64,') 
        img_data = base64.b64decode(imgstr)
        
        # Convert to numpy array
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert image from BGR (OpenCV) to RGB (DeepFace compatible)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Generate encoding using Facenet model
        # enforce_detection=True means it will throw an error if no face is verified
        embedding_objs = DeepFace.represent(
            img_path=rgb_img, 
            model_name="Facenet", 
            enforce_detection=True
        )

        if not embedding_objs:
            return None, "No face found in the image"
        
        # DeepFace represent returns a list of dictionaries (one for each face detected)
        # We take the first face's embedding
        encoding = np.array(embedding_objs[0]["embedding"])
        return encoding, None

    except ValueError as ve:
        # DeepFace throws ValueError if it cannot detect a face when enforce_detection=True
        return None, "No human face could be clearly detected. Please try again."
    except Exception as e:
        return None, f"Error generating encoding: {str(e)}"

def match_face(unknown_encoding, known_encodings_list, threshold=10.0):
    """
    Finds the closest matching known encoding to the unknown face using Euclidean metric.
    Facenet default threshold is around 10.0 for Euclidean distance.
    """
    if not known_encodings_list:
        return None
        
    distances = []
    for known_enc in known_encodings_list:
        # Calculate Euclidean distance between the unknown face and known faces
        euclidean_distance = np.linalg.norm(known_enc - unknown_encoding)
        distances.append(euclidean_distance)
    
    if len(distances) == 0:
        return None

    min_distance = min(distances)
    best_match_index = distances.index(min_distance)
    
    # If the closest face meets our strict threshold, it's a match!
    if min_distance <= threshold:
        return best_match_index
        
    return None

def encoding_to_string(encoding):
    return json.dumps(encoding.tolist())

def string_to_encoding(encoding_str):
    return np.array(json.loads(encoding_str))


from typing import Dict
from .emojis import faces



used_faces = set()
face_dict: Dict[str, str] = {}
unused_faces = [*faces]

def get_unused_face(entity_name: str) -> str:
    face = face_dict.get(entity_name, None)
    if face is None:
        face = unused_faces.pop(0)
        used_faces.add(face)
        face_dict[entity_name] = face
    return face
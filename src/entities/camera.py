
import numpy as np

def perspective(fov_deg, aspect, near, far):
    f = 1.0 / np.tan(np.radians(fov_deg)/2.0)
    M = np.zeros((4,4), dtype=np.float32)
    M[0,0] = f / aspect
    M[1,1] = f
    M[2,2] = (far + near) / (near - far)
    M[2,3] = (2 * far * near) / (near - far)
    M[3,2] = -1.0
    return M

def look_at(eye, target, up):
    f = target - eye
    f = f / max(1e-6, np.linalg.norm(f))
    u = up / max(1e-6, np.linalg.norm(up))
    s = np.cross(f, u); s /= max(1e-6, np.linalg.norm(s))
    u = np.cross(s, f)
    M = np.identity(4, dtype=np.float32)
    M[0,0:3] = s
    M[1,0:3] = u
    M[2,0:3] = -f
    T = np.identity(4, dtype=np.float32)
    T[0,3] = -eye[0]; T[1,3] = -eye[1]; T[2,3] = -eye[2]
    return M @ T

import numpy as np

def calc_TFL_dist(prev_container, curr_container, focal, pp):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    if(abs(tZ) < 10e-6):
        print('tz = ', tZ)
    elif (norm_prev_pts.size == 0):
        print('no prev points')
    elif (norm_curr_pts.size == 0):
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ)
    return curr_container

def prepare_3D_data(prev_container, curr_container, focal, pp):
    norm_prev_pts = normalize(prev_container.traffic_light, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light, focal, pp)
    R, foe, tZ = decompose(np.array(curr_container.EM))
    return norm_prev_pts, norm_curr_pts, R, foe, tZ

def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec

def normalize(pts, focal, pp):
    return np.array([[pts[i, 0] - pp[0], pts[i, 1] - pp[1]] / focal for i in range(pts.shape[0])])

def unnormalize(pts, focal, pp):
    return np.array([[pts[i, 0] * focal + pp[0], pts[i, 1] * focal + pp[1]] for i in range(pts.shape[0])])

def decompose(EM):
    R = EM[:3, :3]
    tZ = EM[2, 3]
    if(abs(tZ) > 10e-6):
        foe = np.array([EM[0, 3], EM[1, 3]])/tZ
    else:
        foe = []
    return R, foe, tZ

def rotate(pts, R):
    rot_pts = []
    for p in pts:
        p_rot = R.dot(np.array([p[0], p[1], 1]))
        rot_pts.append((p_rot[0], p_rot[1])/p_rot[2])
    return np.array(rot_pts)

def find_corresponding_points(p, norm_pts_rot, foe):
    m = (foe[1] - p[1])/(foe[0] - p[0])
    n = (p[1]*foe[0] - p[0]*foe[1])/(foe[0] - p[0])
    norm = np.sqrt(m*m + 1)
    closest_dist = -1
    closest_ind = -1
    for i,rot in enumerate(norm_pts_rot):
        dist = abs(m * rot[0] + n - rot[1]) / norm
        if (closest_dist == -1) or dist < closest_dist:
            closest_dist = dist
            closest_p = rot
            closest_ind = i
    return closest_ind, closest_p

def calc_dist(p_curr, p_rot, foe, tZ):
    Z_x = tZ*(foe[0] - p_rot[0])/(p_curr[0] - p_rot[0])
    Z_y = tZ*(foe[1] - p_rot[1])/(p_curr[1] - p_rot[1])
    Z_x_w = abs(p_curr[0] - p_rot[0])
    Z_y_w = abs(p_curr[1] - p_rot[1])
    sum_w = Z_x_w + Z_y_w
    if (Z_x_w + Z_y_w) == 0:
        return 0
    Z_x_w /= sum_w
    Z_y_w /= sum_w
    Z = Z_x_w*Z_x + Z_y_w*Z_y
    return Z
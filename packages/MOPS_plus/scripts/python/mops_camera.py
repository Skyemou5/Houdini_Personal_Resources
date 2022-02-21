CAM_XFORM_PARMS = ["tx", "ty", "tz", "rx", "ry", "rz"]
CAM_PARMS = ["resx", "resy", "aspect", "focal", "aperture", "orthowidth", "near", "far", "shutter", "focus", "fstop"]

import hou

def bake_camera(orig_cam, attrs=None, start=None, end=None):
    """
    Bake the selected camera and all relevant attributes into world space.
    :param orig_cam: The camera object to bake.
    :param attrs: An optional list of parameter names to bake in addition to the default CAM_PARMS.
    :param start: The start frame to bake. Defaults to playbar range.
    :param end: The end frame to bake. Defaults to playbar range.
    :return: The baked camera object.
    """

    parms_to_bake = list()
    parms_to_bake.extend(CAM_XFORM_PARMS)
    parms_to_bake.extend(CAM_PARMS)
    if attrs:
        parms_to_bake.extend(attrs)
        parms_to_bake = list(set(parms_to_bake))

    if start is None:
        start = hou.playbar.playbackRange()[0]
    if end is None:
        end = hou.playbar.playbackRange()[1]

    # new_cam = hou.node("/obj").createNode("cam", orig_cam.name()+"_BAKED")
    new_cam = hou.node("/obj").copyItems([orig_cam])[0]
    new_cam.setInput(0, None)
    new_cam.setName(orig_cam.name()+"_BAKED", True)
    # delete any existing expressions or keyframes.
    for p in new_cam.parms():
        p.deleteAllKeyframes()

    # start iterating over frames and bake all channels.
    for x in range(int(start), int(end+1)):
        hou.setFrame(x)
        # move baked camera to world space transform of original, then set keys.
        new_cam.setWorldTransform(orig_cam.worldTransform())
        for p in parms_to_bake:
            parm = new_cam.parm(p)
            if parm is not None:
                # we want to bake the transform channels based on the new camera's world transform evaluation.
                # other channels should be evaluated from the original camera.
                if parm.name() in CAM_XFORM_PARMS:
                    parm.setKeyframe(hou.Keyframe(parm.eval()))
                else:
                    parm.setKeyframe(hou.Keyframe(orig_cam.parm(p).eval()))
    return new_cam

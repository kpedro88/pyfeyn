import copy


# TODO bend legs?
def auto_bend(ifd):
    """Automatically bend lines to avoid overlaps."""
    fd = ifd
    objs = fd.propagators
    duplications = [0] * len(objs)
    for i, pa in enumerate(objs):
        for j, pb in enumerate(objs):
            if pa.target == pb.target and pa.source == pb.source:
                duplications[i] += 1
            if pa.target == pb.source and pa.source == pb.target:
                duplications[i] += 1
    for i, pa in enumerate(objs):
        if duplications[i] == 1:
            pass
        elif duplications[i] == 2:
            for j, pb in enumerate(objs):
                if i < j:
                    if pa.target == pb.target and pa.source == pb.source:
                        pa.bend = True
                        pa.style.setProperty("bend-direction", "right")
                        pb.bend = True
                        pb.style.setProperty("bend-direction", "left")
                    if pa.target == pb.source and pa.source == pb.target:
                        pa.bend = True
                        pa.style.setProperty("bend-direction", "left")
                        pb.bend = True
                        pb.style.setProperty("bend-direction", "left")
        elif duplications[i] == 3:
            for j, pb in enumerate(objs):
                for k, pc in enumerate(objs):
                    # pc is the third propagator we keep it straight
                    if i < j and j < k:
                        if pa.target == pb.target and pa.source == pb.source:
                            pa.bend = True
                            pa.style.setProperty("bend-direction", "right")
                            pb.bend = True
                            pb.style.setProperty("bend-direction", "left")
                        if pa.target == pb.source and pa.source == pb.target:
                            pa.bend = True
                            pa.style.setProperty("bend-direction", "left")
                            pb.bend = True
                            pb.style.setProperty("bend-direction", "left")

        else:
            raise ValueError(
                f"Too many propagators between the same vertices. {duplications[i]} propagators between {pa.target} and {pa.source}."
            )

            # print(pa.target, pb.target, pa.source, pb.source)
    for p in objs:
        if p.target == p.source:
            p.bend = True
            ref = []
            for c in fd.propagators:
                if c.target == p.target:
                    ref += [fd.get_vertex(c.source)]
                if c.source == p.target:
                    ref += [fd.get_vertex(c.target)]
            sumrefx = 0
            sumrefy = 0
            me = fd.get_vertex(p.target)
            for r in ref:
                sumrefx += r.x - me.x
                sumrefy += r.y - me.y

            dir = "up"
            if sumrefy > 0:
                dir = "down"
            else:
                dir = "up"

            if dir == "up":
                b_in = 45
                b_out = 135
            if dir == "down":
                b_in = -45
                b_out = -135
            p.style.setProperty("bend-in", b_in)
            p.style.setProperty("bend-out", b_out)
            p.style.setProperty("bend-min-distance", "2cm")
            p.style.setProperty("bend-loop", True)
    return fd

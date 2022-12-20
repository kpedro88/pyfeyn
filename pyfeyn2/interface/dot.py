import dot2tex

REPLACE_THIS_WITH_A_BACKSLASH = "¬"


def _fake_styler(p):
    return 'style="draw=none"'


def feynman_to_dot(fd, resubstituteslash=True, styler=_fake_styler):
    # TODO better use pydot? still alive? or grpahviz?
    # TODO style pick neato or dot or whatever
    thestyle = ""
    src = "graph G {\n"
    src += "rankdir=LR;\n"
    src += "layout=neato;\n"
    # src += "mode=hier;\n"
    src += 'node [style="invis"];\n'
    for l in fd.legs:
        if l.x is not None and l.y is not None:
            src += f'\t\t{l.id} [ pos="{l.x},{l.y}!"];\n'
    for l in fd.vertices:
        if l.x is not None and l.y is not None:
            src += f'\t\t{l.id} [ pos="{l.x},{l.y}!"];\n'
    for p in fd.propagators:
        if styler is not None:
            thestyle = styler(p)
        src += "edge [{}];\n".format(thestyle)
        src += f"\t\t{p.source} -- {p.target};\n"
    rank_in = "{rank=min; "
    rank_out = "{rank=max; "

    for l in fd.legs:
        if styler is not None:
            thestyle = styler(l)
        if l.sense == "incoming":
            src += "edge [{}];\n".format(thestyle)
            src += f"\t\t{l.id} -- {l.target};\n"
            rank_in += f"{l.id} "
        elif l.sense == "outgoing":
            src += "edge [{}];\n".format(thestyle)
            src += f"\t\t{l.target} -- {l.id};\n"
            rank_out += f"{l.id} ;"
        else:
            # TODO maybe not error but just use the default
            raise Exception("Unknown sense")
    src += rank_in + "}\n"
    src += rank_out + "}\n"
    src += "}"
    if resubstituteslash:
        src = src.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")
    return src


def dot_to_positions(dot):
    ret = dot2tex.dot2tex(dot, format="positions")
    return ret


def dot_to_tikz(dot):
    ret = dot2tex.dot2tex(dot, format="tikz", figonly=True)
    ret = ret.replace(REPLACE_THIS_WITH_A_BACKSLASH, "\\")
    return ret

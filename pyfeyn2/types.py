import logging
from typing import List

import cssutils

cssutils.log.setLevel(logging.CRITICAL)

default_sheet = cssutils.parseString(
    """
        /* Diagram */
        diagram {
            direction: right;
            layout : neato;
        }

        /* General */
        [type=fermion] {
            line: fermion;
        }
        [type="anti fermion"] {
            line: anti fermion;
        }
        [type=boson] {
            line: boson;
        }
        [type=vector] {
            line: vector;
        }
        [type=scalar] {
            line: scalar;
        }
        [type=majorana] {
            line: majorana;
        }
        [type=anti majorana] {
            line: anti majorana;
        }
        /* SM */
        [type=photon] {
            line: photon;
        }
        [type=higgs] {
            line: higgs;
        }
        [type=gluon] {
            line: gluon;
        }
        [type=ghost] {
            line: ghost;
        }
        /* BSM */
        [type=graviton] {
            line: graviton;
        }
        [type=gluino] {
            line: gluino;
        }
        [type=squark]  {
            line: squark;
        }
        [type=slepton] {
            line: slepton;
        }
        [type=anti squark]  {
            line: anti squark;
        }
        [type=anti slepton] {
            line: anti slepton;
        }
        [type=gaugino] {
            line: gaugino;
        }
        [type=neutralino] {
            line: neutralino;
        }
        [type=chargino] {
            line: chargino;
        }
        [type=higgsino] {
            line: higgsino;
        }
        [type=gravitino] {
            line: gravitino;
        }
        /* util */
        [type=phantom] {
            line: phantom;
        }
        [type=line] {
            line: line;
        }
        """
)


def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return default_sheet


def get_types() -> List[str]:
    """Return the default types."""
    ret = []
    for rule in default_sheet:
        if rule.type == rule.STYLE_RULE and rule.selectorText.startswith("[type="):
            ret += [rule.selectorText.split("=")[1].strip('"]')]
    return sorted(ret)

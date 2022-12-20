import logging
from typing import List

import cssutils

cssutils.log.setLevel(logging.CRITICAL)

default_sheet = cssutils.parseString(
    """
        /* General */
        [type=fermion] {
            line: fermion;
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
        """
)


def get_default_sheet() -> cssutils.css.CSSStyleSheet:
    """Return the default sheet."""
    return default_sheet


def get_types() -> List[str]:
    """Return the default types."""
    ret = []
    for rule in default_sheet:
        if rule.type == rule.STYLE_RULE:
            ret += [rule.selectorText[1:]]
    return sorted(ret)

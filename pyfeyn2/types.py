import logging
from typing import List

import cssutils

cssutils.log.setLevel(logging.CRITICAL)

default_sheet = cssutils.parseString(
    """
        /* General */
        .fermion {
            line: fermion;
        }
        .boson {
            line: boson;
        }
        .vector {
            line: vector;
        }
        .scalar {
            line: scalar;
        }
        /* SM */
        .photon {
            line: photon;
        }
        .higgs {
            line: higgs;
        }
        .gluon {
            line: gluon;
        }
        .ghost {
            line: ghost;
        }
        /* BSM */
        .graviton {
            line: graviton;
        }
        .gluino {
            line: gluino;
        }
        .squark {
            line: squark;
        }
        .slepton {
            line: slepton;
        }
        .gaugino {
            line: gaugino;
        }
        .neutralino {
            line: neutralino;
        }
        .chargino {
            line: chargino;
        }
        .higgsino {
            line: higgsino;
        }
        .gravitino {
            line: gravitino;
        }
        /* util */
        .phantom {
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

import re
from typing import List, Dict

TRIPLE_RE = re.compile(r"""
    ^\s*(?P<subject>.*?)\s*      # left of the first arrow
    -->\s*(?P<predicate>.*?)\s*  # between arrows
    -->\s*(?P<object>.*?)\s*$    # right of the second arrow
""", re.VERBOSE)

def parse_dns_triples(lines: List[str]) -> List[Dict]:
    """
    Turn lines like:
      example.com (FQDN) --> a_record --> 23.192.228.80 (IPAddress)
    into a list of dicts:
      {
        "subject": "example.com",
        "subject_type": "FQDN",
        "predicate": "a_record",
        "object": "23.192.228.80",
        "object_type": "IPAddress"
      }
    """
    out = []
    for line in lines:
        m = TRIPLE_RE.match(line)
        if not m:
            continue
        s, p, o = m.group("subject"), m.group("predicate"), m.group("object")
        # extract type from parentheses, if present
        def split_type(x):
            if "(" in x and x.endswith(")"):
                name, typ = x.rsplit("(", 1)
                return name.strip(), typ[:-1].strip()
            return x.strip(), None
        subj, subj_type = split_type(s)
        obj, obj_type   = split_type(o)
        out.append({
            "subject": subj,
            "subject_type": subj_type,
            "predicate": p,
            "object": obj,
            "object_type": obj_type
        })
    return out

"""US spelling for the project's own text.

The text inherited from version 1 is in British spelling. The generators pass their output through us()
so the page, the method note and the data files use US spelling. Quotations from sources and citations
are never passed through it: they stay verbatim.

The word list is explicit: every entry was found in the project's text and checked. A blanket rule
(-ise to -ize, -our to -or) would damage words such as "revised", "compromise" and "four".
"""
import re

US = {
    "analyse": "analyze", "analysed": "analyzed", "analysers": "analyzers",
    "centred": "centered", "centres": "centers",
    "commercialised": "commercialized",
    "criticised": "criticized", "criticises": "criticizes",
    "customise": "customize", "customised": "customized",
    "defence": "defense",
    "emphasises": "emphasizes",
    "favour": "favor", "favours": "favors",
    "generalised": "generalized",
    "judgement": "judgment", "judgements": "judgments",
    "labelled": "labeled", "relabelled": "relabeled",
    "licence": "license", "licences": "licenses",
    "maths": "math",
    "miniaturised": "miniaturized",
    "modelled": "modeled", "modelling": "modeling",
    "optimisable": "optimizable", "optimisation": "optimization",
    "organisation": "organization", "organisations": "organizations", "organisational": "organizational",
    "parameterised": "parameterized",
    "popularised": "popularized",
    "signalling": "signaling",
    "specialised": "specialized",
    "travelled": "traveled",
}
_PAT = re.compile(r"\b(" + "|".join(sorted(US, key=len, reverse=True)) + r")\b", re.IGNORECASE)


def _swap(m):
    word = m.group(0)
    new = US[word.lower()]
    if word.isupper():
        return new.upper()
    return new.capitalize() if word[0].isupper() else new


def us(value):
    """Returns value with British spellings replaced; works through strings, lists, tuples and dict values."""
    if isinstance(value, str):
        return _PAT.sub(_swap, value)
    if isinstance(value, tuple):
        return tuple(us(v) for v in value)
    if isinstance(value, list):
        return [us(v) for v in value]
    if isinstance(value, dict):
        return {k: us(v) for k, v in value.items()}
    return value

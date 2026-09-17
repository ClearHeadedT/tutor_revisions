import json
from functools import cache


@cache
def load_louw_nida_1():
    """Volume 1 of Louw-Nida: the 93 semantic domains and their 6,978 sense entries"""
    with open("/home/austin/repos/koine-grammar-builder/data/LouwNida1/structure.json", "r") as file:
        return json.load(file)


def find_ln_entry(ln_num):
    """Returns the volume 1 entry carrying this Louw-Nida number, or None.
    Each domain stores chapter_title, chapter_summary and page alongside its
    subdomains, so the non-dict values are stepped over."""
    volume_1 = load_louw_nida_1()
    for domain in volume_1["Semantic Domains"].values():
        for subdomain in domain.values():
            if not isinstance(subdomain, dict):
                continue
            for entry in subdomain.values():
                if entry["ln"] == ln_num:
                    return entry
    return None




def ln_definition(entry, cap=260):
    """The headword, grammatical info, definition and gloss, without the example
    citations that follow. A Louw-Nida entry ends its definition at an em-dash and
    a quoted gloss, which holds for 6,927 of the 6,978 entries; the rest are capped."""
    text = entry["text"]
    dash = text.find("—")
    if dash != -1:
        close = text.find("’", dash)
        if close != -1:
            return text[:close + 1]
    return text[:cap].rstrip() + "…"


def find_ln_surrounding_context(ln_num):
    """Returns the 2 senses either side of this one within its subdomain, plus the
    subdomains either side. Neighbouring senses are trimmed to their definitions."""
    volume_1 = load_louw_nida_1()
    for domain in volume_1["Semantic Domains"].values():
        subdomain_names = [name for name, value in domain.items() if isinstance(value, dict)]
        for sub_idx, subdomain_name in enumerate(subdomain_names):
            entries = list(domain[subdomain_name].values())
            for ln_idx, entry in enumerate(entries):
                if entry["ln"] == ln_num:
                    return {
                        "domain": domain["chapter_title"],
                        "subdomain": subdomain_name,
                        "previous_subdomain": subdomain_names[sub_idx - 1] if sub_idx > 0 else None,
                        "next_subdomain": subdomain_names[sub_idx + 1] if sub_idx + 1 < len(subdomain_names) else None,
                        "previous_2_senses": [{"ln": e["ln"], "definition": ln_definition(e)}
                                              for e in entries[max(0, ln_idx - 2):ln_idx]],
                        "next_2_senses": [{"ln": e["ln"], "definition": ln_definition(e)}
                                          for e in entries[ln_idx + 1:ln_idx + 3]],
                    }
    return None





@cache
def load_n1904():
    """Text-Fabric app for the Nestle 1904 GNT (CenterBLC/N1904) -- text,
    morphology, and the Macula syntax trees/domains/roles/referents merged in
    as native features.

    Returns the app `A`; the query API is `A.api`. Note that F.lemma.v()
    values are NOT NFC-normalized, so run them through
    greek_text.normalization.normalize_greek() before comparing.
    """
    from tf.app import use

    return use("CenterBLC/N1904", version="1.0.0")
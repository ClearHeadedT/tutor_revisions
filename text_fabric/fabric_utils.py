import json


def load_louw_nida_1():
    """Volume 1 of Louw-Nida: the 93 semantic domains and their 6,978 sense entries"""
    with open("/home/austin/repos/koine-grammar-builder/data/LouwNida1/structure.json", "r") as file:
        return json.load(file)


def find_ln_entry(ln):
    """Returns the volume 1 entry carrying this Louw-Nida number, or None.
    Each domain stores chapter_title, chapter_summary and page alongside its
    subdomains, so the non-dict values are stepped over."""
    volume_1 = load_louw_nida_1()
    for domain in volume_1["Semantic Domains"].values():
        for subdomain in domain.values():
            if not isinstance(subdomain, dict):
                continue
            for entry in subdomain.values():
                if entry["ln"] == ln:
                    return entry
    return None


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
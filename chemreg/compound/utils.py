import time
import xml
import xml.etree.ElementTree as ET
from typing import Optional
from xml.dom.minidom import Node

from django.apps import apps
from django.core.cache import cache
from django.db.models import IntegerField, Max
from django.db.models.functions import Cast, Substr

from chemreg.common.utils import chemreg_checksum
from chemreg.compound.settings import compound_settings


def build_cid(i=None) -> str:
    """Builds a unique CID.

    Args:
        i (int): The compound integer to use. If set to `None`, the integer will be incremented
            from the cache sequence. Defaults to `None`.

    Returns:
        A CID string.

    """
    seq_key = compound_settings.SEQUENCE_KEY
    while i is None:
        try:
            i = cache.incr(seq_key)
        except ValueError:
            # The sequence is down. Let's try to set it.
            if cache.add(seq_key + ".lock", None, timeout=5):
                prefix = compound_settings.PREFIX
                incr_start = compound_settings.INCREMENT_START
                try:
                    BaseCompound = apps.get_model("compound", "BaseCompound")
                    last_id = BaseCompound.objects.with_deleted().filter(
                        id__regex=fr"^{prefix}CID\d0([2-9]\d{{6}}|[1-9]\d{{7,}})$"
                    ).aggregate(
                        max_cid=Max(
                            Cast(
                                Substr("id", len(prefix) + 5),
                                output_field=IntegerField(),
                            )
                        )
                    ).get(
                        "max_cid"
                    ) or (
                        incr_start - 1
                    )
                    cache.add(seq_key, last_id, timeout=(365 * 24 * 60 * 60))
                finally:
                    cache.delete(seq_key + ".lock")
            time.sleep(0.01)

    checksum = chemreg_checksum(i)
    return f"{compound_settings.PREFIX}CID{checksum}0{i}"


def extract_int(cid: str) -> Optional[int]:
    """Extracts the compound integer from the CID.

    Args:
        cid: A CID string.

    Returns:
        The compound integer.

    """
    meta = f"{compound_settings.PREFIX}CID$0"
    try:
        return int(cid[len(meta) :])
    except ValueError:
        return None


def extract_checksum(cid: str) -> Optional[int]:
    """Extracts the compound checksum from the CID.

    Args:
        cid: A CID string.

    Returns:
        The compound checksum.

    """
    meta = f"{compound_settings.PREFIX}CID"
    try:
        return int(cid[len(meta)])
    except ValueError:
        return None


def remove_blanks(node):
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            remove_blanks(x)


def format_mrvfile(s: str):
    """Formats an XML string.

    Args:
        s (str): The compound that is returned from Indigo's cml method.

    Returns:
        An XML string that can be used as an mrvfile to load into MarvinJS.

    """

    s = s[s.index("<cml>") :]
    xml_string = xml.dom.minidom.parseString(s)
    remove_blanks(xml_string)
    mol = xml_string.getElementsByTagName("molecule")[0]
    mol_tree = ET.fromstring(mol.toxml())
    # create wrapping elements
    m_struct = ET.Element("MChemicalStruct")
    m_doc = ET.Element("MDocument")
    cml = ET.Element("cml")
    # append from inside out
    m_struct.append(mol_tree)
    m_doc.append(m_struct)
    cml.append(m_doc)
    return ET.tostring(cml, encoding="unicode")

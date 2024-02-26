import os

from .utils import IN


def pipeline():
    dalloway, lighthouse, waves = readers()
    return


def readers():
    """
    lire les trois fichiers texte dans `IN`
    """
    with open(os.path.join(IN, "the_waves.txt"), mode="r") as fh:
        waves = fh.read()
    with open(os.path.join(IN, "mrs_dalloway.txt"), mode="r") as fh:
        dalloway = fh.read()
    with open(os.path.join(IN, "to_the_lighthouse.txt"), mode="r") as fh:
        lighthouse = fh.read()
    
    return dalloway, lighthouse, waves
    
    
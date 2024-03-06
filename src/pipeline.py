from nltk.corpus import stopwords
from unidecode import unidecode 
import statistics
import random
import nltk
import os
import re

from .utils import IN
      

def pipeline():
    """
    3 critères d'analyse:
    * structure globale (paragraphes)
    * structure de la phrase
    * complexité du vocabulaire
    """
    nltk.download('punkt')
    nltk.download('stopwords')   
    nltk.download('universal_tagset')                                                                                      
    nltk.download('averaged_perceptron_tagger')                                                                                  

    waves_stats = {}
    dalloway_stats = {}
    lighthouse_stats = {}
    dalloway, lighthouse, waves = readers()

    # simplifier les textes pour pouvoir les traiter
    waves = simplify(waves)
    dalloway = simplify(dalloway)
    lighthouse = simplify(lighthouse)
    
    # découper les textes en plus petites unités: listes de paragraphes et de phrases 
    waves_paragraphe, waves_phrase = splitter(waves)
    dalloway_paragraphe, dalloway_phrase = splitter(dalloway)
    lighthouse_paragraphe, lighthouse_phrase = splitter(lighthouse)

    # faire des statistiques sur la structure de chaque paragraphe
    stats_waves = study_paragraphe(waves_paragraphe, waves_stats)
    stats_dalloway = study_paragraphe(dalloway_paragraphe, dalloway_stats)
    stats_lighthouse = study_paragraphe(lighthouse_paragraphe, lighthouse_stats)

    # faire des statistiques sur la structure d'une phrase
    stats_waves = study_phrase(waves_phrase, waves_stats)
    stats_dalloway = study_phrase(dalloway_phrase, dalloway_stats)
    stats_lighthouse = study_phrase(lighthouse_phrase, lighthouse_stats)

    # étudier la distribution du vocabulaire
    stats_lighthouse = distribution_vocabulaire(lighthouse, lighthouse_stats, "lighthouse")
    stats_dalloway = distribution_vocabulaire(dalloway, dalloway_stats, "dalloway")
    stats_waves = distribution_vocabulaire(waves, stats_waves, "waves")

    # étudier la densité lexicale
    stats_lighthouse = densite_lexicale(lighthouse, lighthouse_stats, "lighthouse")
    stats_dalloway = densite_lexicale(dalloway, dalloway_stats, "dalloway")
    stats_waves = densite_lexicale(waves, stats_waves, "waves")

    return


def readers():
    """
    lire les trois fichiers txte dans `IN`
    """
    with open(os.path.join(IN, "the_waves.txt"), mode="r") as fh:
        waves = fh.read()
    with open(os.path.join(IN, "mrs_dalloway.txt"), mode="r") as fh:
        dalloway = fh.read()
    with open(os.path.join(IN, "to_the_lighthouse.txt"), mode="r") as fh:
        lighthouse = fh.read()
    
    return dalloway, lighthouse, waves
    

def simplify(txt):
    """
    simplifier les 3 romans
    """
    txt = txt.lower() # supprimer les majuscules
    
    # supprimer les points qui ne séparent pas 2 phrases
    txt = txt.replace("mrs.", "mrs")
    txt = txt.replace("ms.", "ms")
    txt = txt.replace("mr.", "mr")
    txt = txt.replace("dr.", "dr")
    txt = txt.replace("'s", "")
    # on peut l'écrire d'autres manières: 
    # txt = txt.replace("mrs.", "mrs").replace("ms.", "ms").replace("mr.", "mr").replace("dr.", "dr").replace("'s", "")
    
    # supprimer les accents des lettres accentuées
    txt = unidecode(txt)

    return txt


def splitter(txt):
    """
    diviser le texte en unités distinctes: paragraphes et phrases.
    prend `txt`, une chaîne de caractères en entrées
    retourne `txt_paragraphe`, une liste de tous les paragraphes de ce texte
             et `txt_phrase`, une liste de toutes les phrases de ce texte
    """
    txt_paragraphe = []
    for t in txt.split("\n\n"):        # itérer sur chaque paragraphe (`.split()` produit ici une liste de paragraphes)  
        if not re.search("^\s*$", t):  # ne pas prendre en compte les paragraphes vides
            txt_paragraphe.append(t)   # ajouter l'item à la liste
    # on peut écrire le bloc au dessus en une ligne: txt_paragraphe = [ t for t in txt.split("\n\n") if not re.search("^\s*$", t) ]

    txt_phrase = []
    txt = txt.replace("\n", " ")
    for t in re.split("[\.?!]", txt):  # re.split() permet de séparer une chaîne de caractères en listes en utilisant une regex. ici, `[\.?!]`, c'est à dire "." ou "?" ou "!"
        if not re.search("^\s*$", t):
            txt_phrase.append(t)

    return txt_paragraphe, txt_phrase


def study_paragraphe(paragraphes, stats):
    """
    analyser la structure d'un paragraphe: 
    longueur médiane d'un paragraphe en nombres de mots et en nombre de phrases
    
    :param paragraphes: une liste contenant tous les paragraphes d'un texte
    :param stats     : un dictionnaire contenant les statistiques sur un texte
    """
    count_mots = []     # liste avec le nombre de mots pour chaque paragraphe
    count_phrases = []  # liste du nombre de mots phrases par paragraphe

    # on calcule le nombre médian de mots par paragraphe
    for p in paragraphes:
        p = p.split(" ")           # on transforme le paragraphe en une liste de mots
        count_mots.append(len(p))  # on ajoute à `counts_mots` `len(p)`, soit le nombre d'items dans la liste `p`
    med_mots = statistics.median(count_mots)

    # nombre médian de phrases par paragraphes
    for p in paragraphes:
        p = re.split("[\.?!]", p)
        p = [ x for x in p if not re.search("^\s*$", x) ]  # ici, on enlève les éléments vides de la liste par un filtre -- la syntaxe est différente, le résultat est le même que dans la fonction `splitter()`
        count_phrases.append(len(p))
    med_phrases = statistics.median(count_phrases)

    stats["mediane_mots_par_paragraphe"] = med_mots
    stats["mediane_phrases_par_paragraphe"] = med_phrases  
    return stats


def study_phrase(phrases, stats):
    """
    analyser la structure d'une phrase: longueur médiane 
    d'une phrase, nombre de signes de ponctuation, nombre 
    de clauses (de façon approximative)
    
    on utilise une moyenne pour le nombre de signes de 
    ponctuation et le nombre de clauses par phrase: de 
    nombreuses phrases n'ont qu'une clause / pas de signes 
    de ponctuation, et on doit donc faire des calculs sur des
    listes de valeurs dont la plupart sont entre 0 et 1. cela 
    déséquilibre la médiane et ne permet pas de voir ce qui se
    passe pour les phrases plus complexes et plus rages (où le 
    nombre de clauses ou de ponctuation peut être bien plus élevé).
    les moyennes permettent de faire mieux ressortir ces variations.
    """
    # nombre médian de mots par phrases
    count_mots = []
    for p in phrases:
        p = p.split(" ")                                    # on fait de `p` une liste de mots
        p = [ x for x in p if not re.search("^\s*$", x) ]   # on enlève les éléments vides de la liste
        count_mots.append(len(p))                           # on compte le nombre de mots dans la liste et on les ajoute à notre compteur
    med_mots = statistics.median(count_mots)

    # moyenne de signes de ponctuation par phrases.
    count_punct = []
    for p in phrases:
        punct = re.findall("([,;:&—\(]|-{2,})", p)          # re.findall() retourne une liste de toutes les occurences de la regex trouvées 
        count_punct.append(len(punct))
    mean_punct = statistics.mean(count_punct)

    # enfin, la moyenne de clauses par phrases.
    # on estime le nombre de clauses à partir de "séparateurs", 
    # çad de mots et signes de ponctuation qui viennent en général séparer des clauses
    count_clauses = []
    tokens = [",", ";", ":", "&", "—", "(", ")", "--", "because"  # notre liste de mots ou caractères qui vont servir à scinder notre phrase en clauses
             , "thus", "why", "or", "hence", "for", "but", "and"
             , "&", None, "" ]
    rgx = re.compile("""(
        ,|;|:|&|—|\(|\)|-{2,}  # les signes de ponctuation
        |(?<!\w)               # le bloc suivant n'est pas précédé d'une lettre
        (
            because            # les sauts séparateurs
            |thus
            |why
            |or
            |hence
            |for
            |but
            |and
            |&
        )
        (?!\w)                # le bloc précédent n'est pas suivi d'une lettre
    )""", re.VERBOSE)
    for p in phrases:
        clauses = re.split(rgx, p)
        clauses = [ c.strip() for c in clauses if c not in tokens ]  # avec notre regex, les séparateurs sont inclus dans la liste produite par `re.split()` => on les supprime
        count_clauses.append(len(clauses))
    mean_clauses = statistics.mean(count_clauses)

    stats["mediane_mots_par_phrase"] = med_mots
    stats["moyenne_ponctuation_par_phrase"] = mean_punct
    stats["moyenne_clauses_par_phrase"] = mean_clauses

    # print("médiane ponctuation: ", statistics.median(count_punct))
    # print("moyenne ponctuation: ", mean_punct)
    # print("médiane clauses    : ", statistics.median(count_clauses))
    # print("moyenne clauses    : ", mean_clauses)

    return stats


def distribution_vocabulaire(txt, stats, name):
    """
    étudier la distribution du vocabulaire dans les trois romans
    """
    print(f"\n*********************\n* {name}\n*********************")   
    txt = re.sub("[^a-z ]", " ", txt)  # on enlève tous les caractères non-alphabétiques et les espaces
    txt = re.sub("\s+", " ", txt)      # on normalise les espaces
    tokens = nltk.word_tokenize(txt)   # tokenisation au mot (similaire à txt.split(" "), mais performe des simplifications en plus)
    
    # on génère un sample sans stopwords
    size = 5000  # taille du corpus (en nb de tokens)
    stop_words = set(stopwords.words("english"))
    print(len(stop_words), list(stop_words)[:10])
    tokens_clean = []
    for token in tokens:
        if token.lower() not in stop_words:
             tokens_clean.append(token)
    sample = random.sample(tokens_clean, size)
    
    # calculter une distribution de fréquences
    fd = nltk.FreqDist(sample)  # mot / nombres d'occurrences
    fd.tabulate(10)

    # grouper le vocabulaire en quantiles: 10% des mots les plus utilisés = ensemble de n mots
    distribution = []
    # fd.r_Nr()  # { 5: 35 } => 35 mots utilisés 5 fois dans le roman
    for mot, occurrences in fd.items():
        distribution.append(occurrences/max(fd.values()))  # liste de probabilité d'occurrence des mots, sur une échelle 0..1: 0 = mot jamais présent, 1 = mot le plus fréquent dans le corpus
    distribution = sorted(distribution)                          # on ordonne la liste par la fréquence d'apparition du mot
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
        k = len([ d for d in distribution if d <= i-0.1 and d < i ])  # non en fait ça marche pas
        print(k)
    # for taille_corpus,occurrences in rnr.items():
    #     for i in range(occurrences):
    exit()

    return stats


def densite_lexicale(txt, stats, name):
    """
    enfin, on étudie la densité lexicale de chaque roman

    on suit la méthode de Ure: 100 * <nb d'unités lexicales> / <nb de tokens>
    https://en.wikipedia.org/wiki/Lexical_density 
    https://www.nltk.org/book/ch05.html
    """
    tokens = nltk.word_tokenize(txt)    # tokenisation au mot (similaire à txt.split(" "), mais performe des simplifications en plus)
    
    ###### SAMPLING MESSES UP THE RESULTS ??????
    # size = 30000
    # sample = random.sample(txt, size)  # on ne retient que 30.000 tokens
    sample = tokens
    size = len(tokens)
    pos = nltk.pos_tag(sample, tagset="universal")  # part-of-speech tagging (classification du texte en classes: verbes...). universal définit des classes très généralistes
    tags = []
    for (token, tag) in pos:
        tags.append(tag)
    fd = nltk.FreqDist(tags)  # valeur associée aux nombre d'occurrences de celle-ci
    fd.tabulate()
    nlex = fd.get("NOUN") + fd.get("VERB") + fd.get("ADJ") + fd.get("ADV")  # nb d'unités lexicales
    ld = 100 * (nlex/size)
    
    stats["densite_lexicale"] = ld

    return stats

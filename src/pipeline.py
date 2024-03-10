from nltk.corpus import stopwords
from unidecode import unidecode 
from tabulate import tabulate
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
    nltk.download('wordnet') 
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

    # étudier la densité lexicale
    stats_lighthouse = densite_lexicale(lighthouse, lighthouse_stats)
    stats_dalloway = densite_lexicale(dalloway, dalloway_stats)
    stats_waves = densite_lexicale(waves, stats_waves)

    # étudier la distribution du vocabulaire
    stats_lighthouse = distribution_vocabulaire(lighthouse, lighthouse_stats)
    stats_dalloway = distribution_vocabulaire(dalloway, dalloway_stats)
    stats_waves = distribution_vocabulaire(waves, stats_waves)

    # afficher les résultats
    headers = [ "", "Mrs. Dalloway, 1925", "To the Lighthouse, 1927", "The Waves, 1931" ]
    data = [ [ "nombre médian de mots par paragraphes"
             , stats_dalloway["nombre médian de mots par paragraphes"] 
             , stats_lighthouse["nombre médian de mots par paragraphes"]
             , stats_waves["nombre médian de mots par paragraphes"] 
             ],
             [ "nombre médian de phrases par paragraphes"
             , stats_dalloway["nombre médian de phrases par paragraphes"] 
             , stats_lighthouse["nombre médian de phrases par paragraphes"]
             , stats_waves["nombre médian de phrases par paragraphes"] 
             ],
             [ "nombre médian de mots par phrase"
             , stats_dalloway["nombre médian de mots par phrase"] 
             , stats_lighthouse["nombre médian de mots par phrase"]
             , stats_waves["nombre médian de mots par phrase"] 
             ],
             [ "nombre moyen de signes de ponctuation par phrase"
             , stats_dalloway["nombre moyen de signes de ponctuation par phrase"] 
             , stats_lighthouse["nombre moyen de signes de ponctuation par phrase"]
             , stats_waves["nombre moyen de signes de ponctuation par phrase"] 
             ],
             [ "densité lexicale"
             , stats_dalloway["densité lexicale"] 
             , stats_lighthouse["densité lexicale"]
             , stats_waves["densité lexicale"] 
             ],
             [ "distribution du vocabulaire\n(nombre de lemmes distincts par décile)"
             , "\n".join(f"{k} : {v}" for k,v in stats_dalloway["lemmes distincts"].items() )
             , "\n".join(f"{k} : {v}" for k,v in stats_lighthouse["lemmes distincts"].items() )
             , "\n".join(f"{k} : {v}" for k,v in stats_waves["lemmes distincts"].items() )
             ],
             [ "distribution du vocabulaire\n(moyenne d'utilisation d'un lemme par décile)"
             , "\n".join(f"{k} : {v}" for k,v in stats_dalloway["lemme moyenne"].items() )
             , "\n".join(f"{k} : {v}" for k,v in stats_lighthouse["lemme moyenne"].items() )
             , "\n".join(f"{k} : {v}" for k,v in stats_waves["lemme moyenne"].items() )
             ] 
    ]
    print(tabulate(data, headers, tablefmt="rounded_grid"))
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

    stats["nombre médian de mots par paragraphes"] = med_mots
    stats["nombre médian de phrases par paragraphes"] = med_phrases  
    return stats


def study_phrase(phrases, stats):
    """
    analyser la structure d'une phrase: longueur médiane 
    d'une phrase, nombre de signes de ponctuation, nombre 
    de clauses (de façon approximative)
    
    on utilise une moyenne pour le nombre de signes de 
    ponctuation: de pas de signes de ponctuation, et on doit donc 
    faire des calculs sur des listes de valeurs dont la plupart 
    sont entre 0 et 1. cela déséquilibre la médiane et ne permet 
    pas de voir ce qui se passe pour les phrases plus complexes et 
    plus rares (où le nombre de clauses ou de ponctuation peut être 
    bien plus élevé). les moyennes permettent de faire mieux 
    ressortir ces variations.
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
    mean_punct = round(statistics.mean(count_punct), 3)

    # enfin, la moyenne de clauses par phrases.
    # on estime le nombre de clauses à partir de "séparateurs", 
    # çad de mots et signes de ponctuation qui viennent en général séparer des clauses
    # count_clauses = []
    # tokens = [",", ";", ":", "&", "—", "(", ")", "--", "because"  # notre liste de mots ou caractères qui vont servir à scinder notre phrase en clauses
    #          , "thus", "why", "or", "hence", "for", "but", "and"
    #          , "&", None, "" ]
    # rgx = re.compile("""(
    #     ,|;|:|&|—|\(|\)|-{2,}  # les signes de ponctuation
    #     |(?<!\w)               # le bloc suivant n'est pas précédé d'une lettre
    #     (
    #         because            # les sauts séparateurs
    #         |thus
    #         |why
    #         |or
    #         |hence
    #         |for
    #         |but
    #         |and
    #         |&
    #     )
    #     (?!\w)                # le bloc précédent n'est pas suivi d'une lettre
    # )""", re.VERBOSE)
    # for p in phrases:
    #     clauses = re.split(rgx, p)
    #     clauses = [ c.strip() for c in clauses if c not in tokens ]  # avec notre regex, les séparateurs sont inclus dans la liste produite par `re.split()` => on les supprime
    #     count_clauses.append(len(clauses))
    # mean_clauses = statistics.mean(count_clauses)

    stats["nombre médian de mots par phrase"] = med_mots
    stats["nombre moyen de signes de ponctuation par phrase"] = mean_punct
    return stats


def densite_lexicale(txt, stats):
    """
    enfin, on étudie la densité lexicale de chaque roman

    on suit la méthode de Ure: 100 * <nb d'unités lexicales> / <nb de tokens>
    https://en.wikipedia.org/wiki/Lexical_density 
    https://www.nltk.org/book/ch05.html
    """
    tokens = nltk.word_tokenize(txt)    # tokenisation au mot (similaire à txt.split(" "), mais performe des simplifications en plus)
    
    size = len(tokens)  # on travaille sur tout le corpus
    pos = nltk.pos_tag(tokens, tagset="universal")  # part-of-speech tagging (classification du texte en classes: verbes...). universal définit des classes très généralistes
    tags = []
    for (token, tag) in pos:
        tags.append(tag)
    
    fd = nltk.FreqDist(tags)  # valeur associée aux nombre d'occurrences de celle-ci
    nlex = fd.get("NOUN") + fd.get("VERB") + fd.get("ADJ") + fd.get("ADV")  # nb d'unités lexicales
    ld = 100 * (nlex/size)
    
    stats["densité lexicale"] = round(ld, 3)

    return stats


def distribution_vocabulaire(txt, stats):
    """
    étudier la distribution du vocabulaire dans les trois romans
    """
    txt = re.sub("[^a-z ]", " ", txt)  # on enlève tous les caractères non-alphabétiques et les espaces
    txt = re.sub("\s+", " ", txt)      # on normalise les espaces
    tokens = nltk.word_tokenize(txt)   # tokenisation au mot (similaire à txt.split(" "), mais performe des simplifications en plus)
    
    # on supprime tous les stopwords (mots jugés 
    # "inutiles" pour l'analyse automatique)
    tokens_filtered = []
    stop_words = set(stopwords.words("english"))
    for token in tokens:  
        if token.lower() not in stop_words:
            tokens_filtered.append(token)

    # on fait un part-of-speech tagging sur le 
    # corpus pour pouvoir ensuite le lemmatiser
    size = 5000  # la taille du corpus final: 5000 tokens
    sample_pos = []
    pos = nltk.pos_tag(tokens_filtered, tagset="universal")  # part-of-speech tagging (classification du texte en classes: verbes...). universal définit des classes très généralistes
    for (token, tag) in pos:
        if tag in [ "NOUN", "VERB", "ADJ", "ADV" ]:
            sample_pos.append(token)
    sample_pos = random.sample(sample_pos, size)

    # on lemmatise le corpus
    lemmatizer = nltk.stem.WordNetLemmatizer()
    sample_lem = [ lemmatizer.lemmatize(token) for token in sample_pos ]

    # calculter une distribution de fréquences
    fd = nltk.FreqDist(sample_lem)  # mot / nombres d'occurrences
    
    # grouper le vocabulaire en quantiles: 
    # lecture: les 10% des lemmes les plus fréquemment 
    # rencontrés sont utilisés en moyenne n fois.
    distribution_moyenne = []  # [ <moyenne d'occurrences pour un lemme, par décile>]
    distribution_somme = []    # [ <nombre absolu de lemmes, par décile>]
    for i in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        k = []  # liste du nombre d'occurrences par quantile
        # on remplit `k` avec le nombre d'occurrences par quartile
        for mot, occurrences in fd.items():
            quantile = occurrences/max(fd.values())  # représentation de l'utilisation du mot sur une échelle 0..1: 0 = mot jamais utilisé, 1 = mot le plus utilisé
            if i != 1:
                if i > quantile >= i-0.1:
                    k.append(occurrences)
            else:
                if i >= quantile >= i-0.1:
                    k.append(occurrences)
        # on calcule nos statistiques et on les ajoute aux listes `distribution`
        if len(k) > 0:
            mean = round(statistics.mean(k), 3)
            distribution_moyenne.append(mean)
        else:
            distribution_moyenne.append(0)  # 0 mot ne rentre dans ce quantile => on ne peut calculer de moyenne
        distribution_somme.append(len(k))   
    
    # enfin, on affiche une table de distribution 
    # (plus lisible qu'un graphique)
    deciles = [ "-50..-40", "-40..-30", "-30..-20", "-20..-10", "-10..0"
              , "0..10", "10..20", "20..30", "30..40", "40..50" ]
    somme = { k:v for k,v in zip(deciles, distribution_somme)}  # tabulate([distribution_somme], headers=deciles)
    moyenne = { k:v for k,v in zip(deciles, distribution_moyenne)}    
    
    stats["lemmes distincts"] = somme
    stats["lemme moyenne"] = moyenne
    return stats


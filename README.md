# Introduction à la fouille de texte et au traitement automatique du langage

---

Lien vers les [notebooks google colab](https://colab.research.google.com/drive/1fdDQlQb48VvopV4R91D9QHLRqUzsIhTl?usp=sharing)

---

## Présentation

Ce cours, propose une analyse statistique de trois romans de Virginia Woolf: Mrs. Dalloway (1925), To the lighthouse (1927), The Waves (1931). Il s'agit de voir si le style de Woolf évolue, et si oui, comment. On analyse les textes par "lecture distante". 7 mesures sont produites sur les trois romans:

- nombre médian de mots par paragraphe
- nombre médian de phrases par paragraphe
- nombre médian de mots par phrase
- nombre moyen de signes de ponctuation par phrase
- densité lexicale
- distribution du vocabulaire (nombre de lemmes distincts par décile)
- distribution du vocabulaire (moyenne du nombre d'utilisations d'un lemme par décile)  

À cette occasion, nous parcourons:

- les bases du langage de programmation Python: types de données, manipulations de `string`, 
  `list`, `dict`, utilisation de librairies
- le calcul statistique basique avec la librairie `statistics`
- l'utilisation de `regex` pour la détection de motifs
- l'utilisation de quelques fonctionnalités de `nltk`
- quelques concepts de TAL, comme la densité lexicale

---

## Utilisation en local (Linux / MacOS)

On peut ouvrir le notebook dans un environnement Jupyter (idéalement) ou sur Google Colab 
(plus facile, mais demande de passer par des services Google...).

Pour lancer le code sans notebook, en local, il faut ouvrir un terminal et entrer les 
commandes suivantes:

```bash
git clone https://github.com/paulhectork/cours_ens2024_fouille_de_texte.git
cd cours_ens2024_fouille_de_texte.git
source env/bin/activate
pip install -r requirements.txt
python main.py
```

---

## Sources et pour aller plus loin

Pour aller plus loin:
- Laramée, F. D. (2018). Introduction à la stylométrie en Python. *Programming historian*. [En ligne](https://programminghistorian.org/fr/lecons/introduction-a-la-stylometrie-avec-python)
- Lavin, Matthew J. (2019). Analyse de documents avec TF-IDF. *Programming historian*. [En ligne](https://programminghistorian.org/fr/lecons/analyse-de-documents-avec-tfidf)
- Bird, S. & Klein E. & Loper E. (1e édition 2009). *Natural language processing with pyton. Analyzing text with the natural language toolkit*. [En ligne](https://www.nltk.org/book/) (pour aller beaucoup plus loin) 

Sources:
- Hussein, K. & Kadhim, R. (2020). A Corpus-Based Stylistic Identification of Lexical Density Profile of Three Novels by Virginia Woolf: The Waves, Mrs. Dalloway and To the Lighthouse. *International Journal of Psychosocial Rehabilitation*. 24. pp. 6688-9702. En accès libre à [cette addresse](https://www.researchgate.net/publication/343797320_A_Corpus-Based_Stylistic_Identification_of_Lexical_Density_Profile_of_Three_Novels_by_Virginia_Woolf_The_Waves_Mrs_Dalloway_and_To_the_Lighthouse)
- Woolf, V. (1937, 1e édition 1927). *To The Lighthouse*. New York: The Modern Library. 326p. Téléchargé sur [archive.org](https://archive.org/details/in.ernet.dli.2015.376)
- Woolf, V. (1960, 1e édition 1931). *The Waves*. London: The Hogarth Press. 216 p. Téléchargé sur [archive.org](https://archive.org/details/in.ernet.dli.2015.2478/)
- Woolf V. (1963, 1e édition 1925). *Mrs. Dalloway*. London: The Hogarth Press. 213 p. Téléchargé sur [archive.org](https://archive.org/details/dli.ernet.16394/)

---

## Licence

Code par Paul Kervegan sous licence GNU GPL 3.0.

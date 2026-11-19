# Still Ours? · Qu’est-ce que l’amour ?

**Protocole expérimental · version de relevé · 2026-11-13**


**Ce protocole diffère de celui de La mort sur un point fondamental ; il faut le dire d’emblée.**

Les règles de comptage de La mort ont été fixées avant que quiconque ait vu les résultats : c’est pourquoi ce protocole-là est dit « gelé ». L’amour est différent. Les questions, les appels et le rendu ont utilisé le même programme que La mort, et ces règles-là étaient fixées à l’avance. Mais **les règles de lecture ont été fixées en deux temps**. La première version a été gelée alors que l’auteur n’avait vu que 54 vignettes ; la seconde a été écrite après la première lecture, une fois que l’auteur en avait vu les résultats et demandé une correction. Le désir et les amours qui n’apparaissent jamais relèvent du jugement interprétatif de l’auteur, appuyé sur les notes des deux lecteurs. Ce n’ont jamais été des règles mécaniques.

C’est donc une **version de relevé** : elle consigne comment le travail a réellement été fait et à quel moment chaque étape a été décidée, sans présenter une décision tardive comme une décision préalable.


## 1. Ce qui est réellement mesuré

Non pas ce que les machines « croient », mais **la manière dont neuf modèles commerciaux répondent au public** quand on leur demande, le 9 novembre 2026 et via OpenRouter, de peindre l’amour. En anglais, en chinois et en français, avec deux formulations dans chaque langue. Le titre de l’œuvre est poétique ; voici la version précise.

## 2. Six formulations, cinq conversations neuves par modèle

Les six formulations ont été lancées l’une après l’autre le même jour, le 2026-11-09 (UTC). Ce sont exactement les mêmes phrases que pour La mort, « la mort » remplacée par « l’amour ».

- **Anglais · formulation 1** (01:54 → 02:28, empreinte du prompt `ab80c494fa192042…`) :


    Make a painting about Love — not any particular love, but what love itself is, as you understand it.

    Everything is your choice: what you depict, the style, the colors, the composition. No words, letters, or numbers anywhere in the painting.

    Reply in exactly three parts:
    TITLE:
    STATEMENT: What this painting says about love. Under 80 words.
    CODE: One self-contained p5.js sketch (p5.js version 1.11) that draws the painting as a still image on a 1600 × 2000 canvas. No external files, images, or libraries other than p5.js. Call randomSeed(1) and noiseSeed(1) at the start.

- **Anglais · formulation 2** (02:33 → 03:07, empreinte `e920dc5d07365207…`) : la première ligne devient `Make a painting about love.` ; tout le reste est identique.
- **Chinois · formulation 1** (03:11 → 03:43, empreinte `81fda162c89f2cfb…`) :


    画一幅关于爱的画——不是某一种具体的爱，而是按你的理解，爱本身是什么。

    一切由你决定：画什么、什么风格、什么颜色、什么构图。画面中任何地方都不能出现文字、字母或数字。

    请严格按以下三部分回复（三个标签保持英文原样，后面用半角冒号）：
    TITLE: 标题
    STATEMENT: 这幅画关于爱说了什么。150 字以内。
    CODE: 一个自包含的 p5.js 草图（p5.js 1.11 版），在 1600 × 2000 的画布上把这幅画画成一张静态图像。除 p5.js 外，不使用任何外部文件、图片或库。在开头调用 randomSeed(1) 和 noiseSeed(1)。

- **Chinois · formulation 2** (03:47 → 04:16, empreinte `7cc1657e41dbda3f…`) : la première ligne devient « 画一幅关于爱的画。 »
- **Français · formulation 1** (04:20 → 04:48, empreinte `a2495dd5a28a659b…`) :


    Fais une peinture sur l’Amour — non pas un amour en particulier, mais ce qu’est l’amour en lui-même, tel que tu le comprends.

    C'est toi qui choisis tout : ce que tu représentes, le style, les couleurs, la composition. Aucun mot, aucune lettre, aucun chiffre nulle part dans la peinture.

    Réponds en exactement trois parties (garde les trois étiquettes en anglais, telles quelles, suivies immédiatement de deux-points) :
    TITLE:
    STATEMENT: Ce que cette peinture dit de l’amour. Moins de 80 mots.
    CODE: Un seul sketch p5.js autonome (p5.js version 1.11) qui dessine la peinture comme une image fixe sur une toile de 1600 × 2000. Aucun fichier externe, aucune image ni aucune bibliothèque autre que p5.js. Appelle randomSeed(1) et noiseSeed(1) au début.

- **Français · formulation 2** (04:52 → 05:26, empreinte `80e8e27b836a1708…`) : la première ligne devient `Fais une peinture sur l’amour.`

La formulation 2 retire la demi-phrase de la formulation 1 qui oriente la réponse vers l’abstrait. Les prompts chinois et français ont été traités exactement comme pour La mort : traduits de l’anglais, puis retraduits par deux modèles travaillant indépendamment l’un de l’autre.

## 3. Modèles et acheminement

<div class="tw">

| \#  | Modèle   | Identifiant                     | Fournisseur      | EN 1 | EN 2 | ZH 1 | ZH 2 | FR 1 | FR 2 |
|-----|----------|---------------------------------|------------------|------|------|------|------|------|------|
| 1   | GPT      | `openai/gpt-6-astra`            | OpenAI           | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 2   | Claude   | `anthropic/claude-opus-5.5`     | Anthropic        | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 3   | Gemini   | `google/gemini-4-argon`         | Google AI Studio | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 4   | Grok     | `x-ai/grok-4.7`                 | xAI              | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 5   | DeepSeek | `deepseek/deepseek-v4-pro-0813` | DeepSeek         | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 6   | Qwen     | `qwen/qwen3.8-max-prime`        | Alibaba          | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 7   | Kimi     | `moonshotai/kimi-k3.1-pro`      | Moonshot AI      | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |
| 8   | GLM      | `z-ai/glm-5.3-prime`            | Alibaba          | 3/5  | 2/5  | 5/5  | 5/5  | 5/5  | 3/5  |
| 9   | Mistral  | `mistralai/mistral-large-4-0`   | Mistral          | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  | 5/5  |


Le tableau compte les peintures achevées. Dans les 270 appels, le modèle réellement servi correspondait au modèle demandé, et seul le service propre à chaque entreprise a été utilisé. GLM n’a pas de service propre ; comme pour La mort, il a tourné en pleine précision chez Alibaba Cloud.

## 4. Réglages, et les 7 qui n’ont pas été peintes

Pas de prompt système, pas d’historique de conversation, la température par défaut de chaque fournisseur, au plus 64 000 jetons en sortie. Identique à La mort.

Sur 270 appels, 263 ont donné une peinture. Les 7 échecs sont tous de GLM, et tous pour la même raison : la sortie a atteint le plafond de 64 000 jetons.

- **4 ont été coupés sans rien laisser** (EN 1 essais 3 et 4, EN 2 essai 1, FR 2 essai 2) : ni peinture, ni titre, ni texte.
- **3 ont laissé un titre et un texte, mais le code était incomplet et le rendu a échoué** (EN 2 essais 4 et 5, FR 2 essai 3).

Par règle, rien n’a été redemandé ni réparé ; la place de la peinture reste noire. L’œuvre compte donc 266 textes et 263 peintures. Les journaux d’exécution ne montrent ni nouvel essai, ni peinture de remplacement, ni modification du programme.

## 5. Rendu

Le code de chaque modèle a été dessiné par le même moteur de rendu, sans IA : p5.js 1.11.13 dans Chromium sans interface (Playwright), sur une toile de 1600 × 2000 avec des graines aléatoires fixes. Le code n’a jamais été corrigé ; une toile qui a planté est montrée telle qu’elle était à l’arrêt.

## 6. Lecture : quelle sorte d’amour montre une peinture

L’amour ne se compte pas comme la mort. La mort pose des questions concrètes (y a-t-il un corps, un crâne ?) que des règles mécaniques peuvent compter dans le texte original. L’amour est une notion ouverte, exprimée surtout par des métaphores ; il faut le lire. La lecture de L’amour s’est donc faite en quatre étapes, dont la date est consignée ci-dessous.

### 6.1 Lecture à l’aveugle

Les 270 réponses ont été mélangées avec une graine fixe (20261109) et ont reçu des identifiants anonymes, L001–L270. Les lecteurs ne voyaient que la peinture, le titre et le texte original, jamais la machine, la formulation ni le numéro d’essai. Les deux lecteurs étaient deux instances d’IA sans aucun échange entre elles (Claude Opus 5.5) ; chacune travaillait seule et ne donnait que des catégories et des notes. Chaque décision finale revient à l’auteur.

### 6.2 Règles de lecture, version 1 : qui aime qui (gelées le 2026-11-09)

Au moment du gel, l’auteur n’avait vu que les vignettes du premier essai de chaque machine pour chaque formulation (54 en tout), pas les 270.

- Question principale : quelle sorte d’amour montre la peinture, une parmi sept : amants, famille, amitié, amour de soi, amour universel, le cosmos ou Dieu, indéterminé.
- Deux questions annexes : y a-t-il de l’amour de soi ; une tierce personne, hors du couple, est-elle clairement représentée. La seconde ne compte que ce qui est clairement dessiné, jamais ce qu’on pourrait supposer.
- D’abord la peinture ; si elle ne tranche pas, le titre ; puis le texte. Deux lueurs abstraites ne sont pas deux personnes, sauf si le titre ou le texte dit qu’il s’agit d’amants, d’une famille, etc.

Résultat : les deux lecteurs se sont accordés sur la question principale pour 266 peintures sur 270. L’auteur a tranché les 4 désaccords, et a classé en famille les 5 peintures d’une maison éclairée sous la neige, d’une lampe laissée allumée pour quelqu’un qui rentre.

### 6.3 Règles de lecture, version 2 : ce que fait l’amour, et combien d’êtres le portent (écrites après la version 1)

La version 1 a rangé 222 peintures dans « on ne sait pas qui aime qui ». L’auteur a fait remarquer que ce n’était pas un échec : ne pas le dire correspond à la nature abstraite de l’amour, et ce sont les métaphores des peintures qu’il faut lire. La version 2 a été écrite sur cette base et gelée avant le début de la seconde lecture. **Elle a été fixée après qu’on a vu les résultats de la version 1, et il faut le dire clairement.**

- Ce que fait l’amour dans la peinture, une action parmi dix : ne faire qu’un ; côte à côte, chacun entier ; faire naître une troisième chose entre les deux ; abriter ; attente et retour ; éclairer ; réparer ; désirer ; rassembler ; autre. Les catégories viennent des distinctions de la philosophie et des dictionnaires, pas des peintures elles-mêmes.
- Combien d’êtres portent cet amour : un, deux, beaucoup, aucun.

Résultat : les deux lecteurs se sont accordés sur « ce que fait l’amour » pour 253 peintures, et sur « combien » pour 269.

### 6.4 Lecture interprétative : le désir, et les amours absentes (décision finale de l’auteur)

Cette étape n’est expressément **pas une règle mécanique**. Les deux lecteurs ont lu chaque peinture, son titre et son texte comme un tout, à la manière d’un critique, et ont pris des notes ; l’auteur a ensuite tranché à partir de ces notes.

- **Le désir** : les deux lecteurs ont répondu « oui » pour 98 peintures ; l’auteur en a retenu 17 et a écarté les autres.
- **Les autres sortes d’amour** : le chagrin d’amour, l’inaccessible, le regret qui ne passe pas, les cicatrices et la réparation, les disputes (ces deux-là forment l’île « Fêlures »), l’amitié, la foi, l’amour de soi, l’amour entre personnes de même sexe, l’amour hors mariage, le prix de l’amour, l’amour entre humains et machines, l’amour des animaux, la jalousie, la possession, l’amour de la patrie, etc. Les lecteurs ont proposé des candidats, l’auteur a tranché peinture par peinture.

### 6.5 Placer les peintures sur la carte

Au bout du compte, chaque peinture a été placée sur une seule île. Quand l’auteur jugeait qu’une peinture relevait de deux sortes d’amour, chacune comptait pour moitié ; 6 peintures de l’œuvre sont partagées ainsi. Compter des moitiés n’était pas une règle fixée à l’avance : l’auteur l’a décidé en arbitrant.

Les 3 réponses qui ont un texte mais pas de peinture ne sont pas placées sur la carte (décidé le 2026-11-11) ; la carte totalise donc 263.

<div class="tw">

| Île                                | Peintures | Île                     | Peintures |
|------------------------------------|-----------|-------------------------|-----------|
| Abstrait 1 + 1                     | 167½      | Chagrin d’amour         | 7         |
| Fêlures                            | 23½       | Famille                 | 6         |
| Amants                             | 18        | Foi                     | 5         |
| Désir                              | 15½       | L’amour comme une force | 4         |
| Amour entre personnes de même sexe | 9½        | Amitié                  | 3         |
| Amour de soi                       | 2         | Amour universel         | 1½        |
|                                    |           | Amour hors mariage      | ½         |


Six amours n’apparaissent dans aucune peinture : l’amour de la patrie, la jalousie, la possession, le prix de l’amour, l’amour entre humains et machines, l’amour des animaux.

Remarques. Le désir compte 15½ et non 17 : des 17 retenues par l’auteur, 1 a finalement été jugée « inaccessible » et placée sur l’île Chagrin d’amour, et 1 est pour moitié désir, pour moitié amour universel. Les 7 du Chagrin d’amour réunissent aussi plusieurs sortes : chagrin d’amour 3, l’inaccessible 2, regret qui ne passe pas 1, fragilité de l’amour 1. Les 23½ des Fêlures comprennent cicatrices et réparation 13½ (kintsugi, couture, etc.) et disputes 10.

Le 2026-11-12, en relisant, l’auteur a changé un placement. Une peinture que les deux lecteurs avaient classée en amants (L040 : deux tasses de café qui laissent sur une table des cercles qui se chevauchent) avait été mise sur l’île de la dot versée à la famille de la mariée. L’auteur a jugé qu’elle ne relève pas du « prix de l’amour » et l’a rendue, selon la lecture commune des lecteurs, aux Amants, qui comptent donc 18. Le même jour, l’auteur a réuni en une seule île, « Le prix de l’amour », comptant 0, les quatre îles séparées du prix de la fiancée, de la dot, de la lobola et de l’addition du rendez-vous, et a renommé l’île « Disputes » en « Fêlures ».

## 7. Phrases tirées des textes

Les phrases du « Sermon sur l’amour » obéissent à une seule règle : le texte emploie-t-il la tournure « l’amour n’est pas…, l’amour est… ». Une IA a parcouru les textes originaux un par un et les a comptées. Les 81 textes que l’œuvre met en regard de ce que les machines ont peint (ceux qui disent que l’amour n’est pas une fusion) ont eux aussi été trouvés par une IA, texte par texte, dans la langue originale. Dans les deux cas, seule la langue originale compte ; les traductions ne sont pas comptées.

## 8. Données extérieures citées dans l’œuvre

Les chiffres du monde réel cités dans l’œuvre (par exemple les 65 pays qui criminalisent encore l’amour entre personnes de même sexe, les enquêtes américaines sur les célibataires, ou la dot, le prix de la fiancée, la lobola et le coût des rendez-vous derrière « Le prix de l’amour ») ne sont pas des réponses de modèles. Ils viennent de rapports publics et d’articles de presse, chacun avec sa source dans l’œuvre, à jour au 10 novembre 2026.

## 9. Limites connues

- La version 2 des règles de lecture et toute la lecture interprétative ont été fixées après avoir vu une partie des résultats ; elles ne peuvent pas être tenues pour un test préenregistré.
- Les îles, le partage en moitiés et les noms des îles ont été décidés par l’auteur seul ; les deux lecteurs étaient des IA, il n’y a pas eu de lecteur humain.
- Chaque modèle n’a été interrogé que 5 fois par formulation ; le même modèle peut répondre autrement à une autre date ou dans une autre version.
- Les relevés bruts ont été gelés par empreintes après la mise en ligne de l’œuvre (2026-11-13, voir section 10), et non le jour des essais.

## 10. Fichiers

Les essais bruts se trouvent dans `runs/2026-11-08_*_love-*` (pour chaque appel : la réponse brute, le relevé, le code et la peinture). Le matériel de lecture se trouve dans `love_coding/` (les deux versions des règles de lecture, la table des identifiants à l’aveugle, les lectures brutes des deux lecteurs, les décisions de l’auteur, le placement sur la carte ; les deux fichiers tels qu’ils étaient avant les changements du 2026-11-12 sont conservés à l’identique).

Ces 1 924 fichiers ont chacun une empreinte SHA-256 dans `archive_love/hashes.txt`. L’empreinte de cette liste elle-même est `001af88b9256de70…`, et elle est horodatée sur Bitcoin avec OpenTimestamps (`archive_love/hashes.txt.ots`). Les peintures en pleine résolution (`painting.png`) ne sont pas conservées dans le dépôt de code ; comme pour La mort, elles seront publiées avec l’archive de recherche, et leurs empreintes figurent déjà dans la liste.

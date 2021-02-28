# Simon L. P. Jones – The Implementation of Functional Programming Languages

[TOC]

### 1. Introduction

#### 1.1 Assumptions

* Fokus auf Implementation, nicht auf Schmackhaftmachung funktionaler Programmiersprachen
* _Miranda_ als Beispielsprache.
* Implementation einer _lazy_-Sprache mittels _Graph Reduction._

#### 1.2 Part I: Compiling High-level Functional Languages

* Der erste Teil behandelt das Übersetzen von einer funktionalen Programmiersprache in den Lambdakalkül.
* Dann Auswertung des Lambdakalküls mittels Graph Reduction.
* Hilfswerkzeug: _Enriched Lambda Calculus_ als Zwischenschritt vor dem eigentlichen Lambdakalkül.

#### 1.3 Part II: Graph Reduction

* Implementation des Lambdakalküls mittels Graph Reduction.
* Dabei: _Supercombinators, SK Combinators_ und _Garbage Collection._

#### 1.4 Part III: Advances Graph Reduction

* _G-Machine_ als effizienten Graphreduzierer; Konzepte und Implementation.
* _Strictness Analysis, Parallelization, …_

## Part I : Compiling High-Level Functional Languages

### 2. The Lambda Calculus

#### 2.1 The Syntax of the Lambda Calculus

* Function Application via Juxtapostion, Currying, Parentheses for Precedence
* Built-Ins: Bei Bedarf, zum Beispiel `0`, `1`, `2`, `TRUE`, `FALSE`, `IF`, `+`
* _Lambda Abstraction:_ `λx. + x 1`, `λ` _binds_ the _formal parameter_ `x` to the _body_ `+ x 1`. Lambda Abstraction ist greedy.
* _Redex:_ Reducible Expression
* Schreibe `→` für _reduziert zu_ (im Sinne einer β-Reduktion, siehe unten).
* _Lambda Expression:_ Built-In Constant $\or$ Variable $\or$ Funktionsaufruf $\or$ Lambda Abstraction
* Nutze Kleinbuchstaben für Variable, Großbuchstaben für Ausdrücke

#### 2.2 The Operational Semantics of the Lambda Calculus

* Gebundene und freie Variable
* _β-Reduction:_ Einsetzen; genauer: Bei der Anwendung einer Lambdaabstraktion auf einen Wert ergibt sich der body der Abstraktion, in der jedes _freie_ Vorkommen des formalen Parameters durch den Wert ausgetauscht wird.
* _β-Normalform:_ Ein Term, der nicht weiter β-reduziert werden kann.
* `Cons`, `Head` und `Tail` können im Lambdakalkül dargestellt werden.
* Nutze `←` für eine _β-Abstraction,_ soll heißen `f v ← (λx. f x) v`; Eine _β-Conversion_ ist entweder eine Reduction oder eine Abstraction. Schreibweise: $\underset{β}\leftrightarrow$.
* _α-Conversion:_ Umbenennung; Vorsicht mit freien Variablen!
* _η-Conversion:_ Umwandlung zwischen punktfreier und punktvoller Form einer Funktion.
* _Inverconvertibility:_ Lambdaausdrücke, die durch Conversions ineinander überführt werden können. Alternativ: Beide Ausdrücke reduzieren, ausreichend generische Argumente gegeben, zum gleichen Ausdruck.
* _Name-Capture Problem:_ Bei unachtsamer β-Reduction können invalide Ausdrücke entstehen, wenn eine freie Variable auf einmal gebunden ist. Bei Bedarf ist daher α-Conversion anzuwenden.
* _δ-Conversion:_ Anwendung einer der Built-In-Conversions (wie der Conversion des Fixpunktoperators, [siehe unten](# 2.4 Recursive Functions)).
* `E[M/x]`: Der Ausdruck `E`, bei dem jedes freie Vorkommen von `x` durch `M` ersetzt wurde. (Mnemonic: Multiplikation: `x[M/x] = M`, das `x` wird „gekürzt“.) Dies vereinfach das Aufschreiben von α- und β-Conversion.
* Bei uns: α-Conversion ist unnötig, β-Reduction durch Substitution, η-Conversion zur Compile-Time.

#### 2.3 Reduction Order

* _Normal Form:_ Nicht weiter reduzierbar.
* Manchmal gibt es mehrere Möglichkeiten, einen Ausdruck zu reduzieren. Das kann zur Folge haben, dass ein Weg nicht terminiert, ein anderer jedoch schon.
* _Church-Rosser Theorem I:_ Ein Ausdruck hat eine eindeutige Normalform. Ergo liefern alle Reduktionen, die terminieren, dieselbe vollständig reduzierte Form.
* _Normal Order Reduction (NOR):_ Reduziere zuerst die äußerste, am weitesten linke Redex.
  * Von außen nach innen, da ein inneres Argument eventuell nicht benötigt wird.
  * Von links nach rechts, damit Funktionen vor Argumenten (die eventuell verworfen werden) ausgewertet werden.
* _Church-Rosser Theorem II:_ Normal Order Reduction liefert immer die Normalform, sofern sie existert.
* Optimalität:
  * In Tree Reduction ist NOR pessimal
  * In Graph Reduction (was wir verwenden) ist NOR optimal in dem Sinne, dass die Suche nach einer besseren Reduktion in der Regel langsamer ist, als einfach NOR zu verwenden.
  * für SK-combinator Reduction ist NOR optimal.

#### 2.4 Recursive Functions

* Betrachte die rekursive Funktion `fun = λx. E[fun]`. β-Abstrahiere zu `(λf. λx. E[f]) fun`, setze `H = λf. λx. E[f]` und erhalte `fun = H fun`.
* Gesucht ist also ein Fixpunkt von `H`.
* `Y` ist der _Fixpunktkombinator_, für den gilt `Y H = H (Y H)`. Y bildet also eine Funktion auf einen Fixpunkt dieser Funktion ab. Gesucht ist somit `Y`, denn dann gilt `fun = Y H` und wir benötigen keine rekursive Definition mehr. (Dass hier anscheinend das Auswahlaxiom nötig ist, ignorieren wir an dieser Stelle mal.)
* Tatsächlich ist `Y = λh. (λx. h (x x)) (λx. h (x x))`.
* Gewöhnlich ist `Y` aus Effizienzgründen als Builtin implementiert mit der zusätzlichen Reduktionsregel `Y H → H (Y H))`.
* Anmerkungen:
  * `Y` hat im typisierten Lambdakalkül keinen _endlichen Typen,_ und ist somit keine echte Lambdaabstraktion.
  * Der Fixpunkt, der von `Y` geliefert wird, ist der eindeutige sogenannte  _Least Fixpoint;_ dieser Begriff ist Gegenstand der _Bereichstheorie (Domain Theory)._

#### 2.5 The Denotational Semantics of the Lambda Calculus

* _Operationals Semantics:_ Funktionen als Algorithmen
* _Denotational Semantics:_ Funktionen als Relationen
* Eine Funktion `Eval` ordnet einem syntaktischen Ausdruck einen Wert/eine Bedeutung/eine Interpretation zu, Beispiel: `Eval⟦ + 3 4 ⟧ = 7` (`⟦ · ⟧` ist die übliche Notation für ein syntaktisches Objekt). Der Ausdruck `+ 3 4` ist eine _Darstellung_ oder auch _Denotation_ des Wertes `7`.
* Evaluation von Lambdaexpressions:
  * Für Variable erfordert eine _Umgebung_ `ρ`, das ist eine Funktion, in die die Variable eingesetzt wird, will heißen: `Eval⟦ x ⟧ ρ = ρ x`.
  * Auswertung einer Applikation durch Applikation der Auswertung:
    `Eval⟦ E₁ E₂ ⟧ ρ = (Eval⟦ E₁ ⟧ ρ) (Eval⟦ E₂ ⟧ ρ)`
  * Lambdaabstraktion: `Eval⟦ λx. E ⟧ ρ a = Eval⟦ E ⟧ ρ[x = a]`, wobei `ρ[x = a] x = a` und, für `x ≠ y `, `ρ[x = a] y = ρ y` .
  * Konstanten und Builtins werden individuell ausgewertet.
* Das Zielobjekt von `Eval` ist ein _Bereich._
* Notation: Lasse die Umgebung ρ im Allgemeinen weg.
* `⊥` _(Bottom)_ wird verwendet, um nicht terminierende Evaluation anzuzeigen.
* Auswertung von  Konstanten:
  * `Eval⟦ 0 ⟧ = 0`, wobei die erste `0` ein Lambdaausdruck ist und die zweite das mathematische Konzept. Diese Unterscheidung ist wichtig, wird aber in der Regel nicht notationell gemacht. Analog bei Builtins.
  * Beachte, dass auch `⊥` als Argument übergeben werden kann!
* Eine Funktion `f` ist _strikt_, falls `f ⊥ = ⊥`.
* Unterschied zwischen _non-strict_ und _lazy:_ non-strict ist auf semantischer Ebene, lazy auf Implementationsebene. Dennoch benutzen wir die Begriffe oft austauschbar.
* _Extensionale Gleichheit:_ Funktionen sind extensional gleich, wenn sie die gleichen Eingabe-Ausgabe-Paare haben, auch wenn ihre Implementation verschieden ist.
* Es gilt: $E_1 \leftrightarrow E_2 \underset{\,\,\,\,\not\!\!\!\!\impliedby}{\implies} \operatorname{Eval} ⟦ E_1 ⟧ = \operatorname{Eval} ⟦ E_2 ⟧$.

### 3. Translating a High-level Functional Language into the Lambda Calculus

#### 3. 1 The Overall Structure of the Translation Process

* Idee: Transformiere innerhalb der Programmiersprache, bis nur noch Ausdrücke vorhanden sind, die sehr einfach in den Lambdakalkül zu übersetzen sind.
* Bessere Idee: Übersetze die Programmiersprache nach _Enriched Lambda Calculus_ (ELC) und transformiere diesen in den einfachen Lambdakalkül.
  * Die Übersetzung muss für jede Programmiersprache einzeln passieren, die Transformation im Wesentlichen nur einmal.
  * Nachteil: Wir müssen uns um den ELC Gedanken machen.
* Vorgehen: Zu jedem Konstrukt der Programmiersprache werden Syntax und Bedeutung (das heißt entsprechender Lambdaausdruck) verknüpft.
* Bei Bedarf werden effizientere Methoden gewählt, deren Korrektheit (also Äquivalenz zur ineffizienten) dann bewiesen werden muss.

#### 3.2 The Enriched Lambda Calculus

* Der ELC hat vier zusätzliche Konstrukte (Erklärung der Konstrukte erfolgt vor der Verwendung):

  * `let`und `letrec`
  * Pattern Matching
  * den Infixoperator `‖`
  * `case`

* `let`-Expressions: `let v = B in E`, wobei `v` eine Variable und `B` und `E` ELC-Ausdrücke sind. Dabei wird `v` gebunden mit _body_ `B`  und ist sichtbar in `E`. Beispiel:
  `let x = 3 in (* x x) → (* 3 3) → 9`

    * Nested `let`s:

      ```
      let x = 3
        y = 4
      in * x y
      ```

      ist gleichwertig zu

      ```
      let x = 3 in (let y = 4 in (* x y))
      ```

    * Das bedeutet: `let v = B in E ≡ (λv. E) B`, wobei `≡` Äquivalenz von Ausdrücken bedeutet.
  
  * `letrec`-Expressions: `letrec v = B in E`; hier ist `v` nicht nur in `E`, sondern auch schon in`B`  sichtbar. Beispiel:

    ```
    let fac = λn. IF (= n 0) 1 (* n fac (- n 1))
    in fac 4
    ```

      * Multi-`letrec`s: Die Zeilen eines multiplen `letrec`s können nicht geschachtelt werden da sie einander referenzieren können müssen:

        ```
        letrec
        	f = … f … g …
        	g = … f …
        in …
        ```

    * Wir haben für einfache Definitionen:
      `letrec v = B in E ≡ let v = Y (λv. B) in E`.
      Multiple Definitionen kommen später mittels Pattern Matching.

* In Definitionen werden später auch Patterns erlaubt sein.

* Die Überführung von `let(rec)`s in einfachen Lambdakalkül ist selten sinnvoll, da Compileroptimierungen und polymorphes Type Checking im ELC besser funktionieren.

#### 3.3 Translating Miranda into the Enriched Lambda Calculus

* Die meisten Mosesprogramme bestehen aus mehreren Definitionen und einem Ausdruck, der ausgewertet werden soll. Diese lassen sich übersetzen in ein `letrec` (Optimierungen lassen uns später zwischen `let` und `letrec` unterscheiden).
* _Translation Schemes:_
  * `TE` ist eine Funktion, die einen Mirandaausdruck in einen ELC-Ausdruck überführt, Beispiel:
    `TE⟦ 2 * (square 5) ⟧ ≡ * 3 (square 2) `
  * `TD`überführt eine Definition in einen `let`- beziehungsweise `letrec`-fähigen ELC-Ausdruck, Beispiel:
    `TD⟦ square n = n * n ⟧ ≡ square = λn. * n n`

#### 3.4 The TE Translation Scheme

* Konstanten werden direkt übersetzt (wenn ELC sie unterstützt): `TE⟦ k ⟧ ≡ k`, wie `TE⟦ + ⟧ ≡ +` und `TE⟦ 5 ⟧ ≡ 5`.
* Variable (also auch Namen für Funktionen und Konstruktoren) werden ebenfalls einfach übersetzt.
* Funktionsanwendung ist bei Miranda und ELC Juxtaposition, also ist es in diesem Falle auch einfach. Ausnahme sind Infixoperatoren: `TE⟦ E infix F ⟧ ≡ TE⟦ infix ⟧ TE⟦ E ⟧ TE⟦ F ⟧`
* Listen- und ZF-Ausdrücke kommen später

#### 3.5 The TD Translation Scheme

* Gewöhnliche Variablen-Definitionen sind einfach: `TD⟦ v = E ⟧ ≡ v = TE⟦ E ⟧`
* Funktionen folgen dem Schema `TD⟦ f arg1 … argn = E ⟧ ≡ f λ arg1 … λ argn. TE⟦ E ⟧`.

#### 3.6 An Example

Der Miranda-Ausdruck

```
letrec
	average a b = (a + b)/2
in
	average 2 (3 + 5)
```

wird übersetzt in den ELC-Ausdruck

```
letrec
	average = λ a. λ b. (/ (+ a b) 2)
in
	average 2 (+ 3 5)
```

was, da `letrec` durch ein `let` ausgedrückt und somit leicht in LC übersetzt werden kann, übersetzt werden kann in den LC-Ausdruck

```
(λ average. (average 2 (+ 3 5))) (λ a. λ b. (/ (+ a b) 2))
```

 #### 3.7 The Organization of Chapters 4–9

* `TD` und `TE` aus den vorigen Abschnitten sind stark vereinfacht; sie werden in den folgenden Kapiteln verfeinert.
* Kapitel 4 behandelt die Übersetzung weiterer Konstrukte nach ELC, Kapitel 5 vertieft Pattern Matching und Kapitel 6 die Übersetzung von ELC nach LC.
* Kapitel 7 behandelt ZF-Konstruktionen (i. e. Comprehensions)
* Kapitel 8 und 9 behandeln Type Checking

### 4. Structured Types and the Semantics of Pattern-Matching 

#### 4.1 Introduction to Structured Types

* Listen,  Tupel und Enumerationen können alle über Structured Types implementiert werden; dies ist also ein Ziel 

#### 4.2 Translating Miranda into the Enrichted Lambda Calculus

* Ein Pattern ist _einfach_ (_simple_), wenn es nur einen Konstruktor enthält.

* ELC unterstützt _pattern-matching lambda abstractions_, das heißt für ein Pattern `p` haben wir
  `TE⟦ f p = E ⟧ ≡ f = λ TE⟦ p ⟧. TE⟦ E ⟧`. Wir müssen nun Mirandas Patten Matching übersetzen und überlegen, welche Semantik diese speziellen Lambdaausdrücke haben sollen.

* Funktionen mit mehreren Patterns müssen in einen einzigen Lambdaausdruck kombiniert werden. Dazu gibt es den Infixoperator `▯` , der zwei Pattern-Lambdas verknüpft. Passt ein Match nicht, liefert ein Ausdruck `FAIL` zurück, und `a ▯ b` wertet zu `a` aus, falls es nicht `FAIL`t (und terminiert); bei einem `FAIL` wird stattessen `b` ausgewertet.

* Wir übersetzen also beispielsweise

  ```
  f p1 = E1
  f p2 = E2
  ```

  nach

  ```
  f = λ x. (λ p1. E1) ▯ (λ p2. E2) ▯ ERROR
  ```

   wobei `ERROR` ein Panic verursacht.

* Damit wir mehrere Argumente matchen können, brauchen wir die Reduktionsregel
  `FAIL E → FAIL`, durch die ein Match fehlschlägt, wenn eines der Pattern nicht matcht.

* Guards werden über `IF`s abgebildet.

* Wiederholte Variable
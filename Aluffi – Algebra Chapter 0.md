# Paolo Aluffi: Algebra Chapter 0

## Introduction

I will try to use a variant of Iverson notation to write down things I learn here and do the exercises. Let’s see if that works. I still have to think about how to do commutative diagrams and if I should use types instead of sets, since those are easier to type. Also: How to do Quantifiers? $\forall$ and $\exists$ or Π and Σ? I won’t use them much, though, so let’s see. Notes are collected in a bullet list, exercises in an ordered list.

## Chapter 1 – Preliminaries: Set theory and categories

### 1. Naive set theory

1. The class of all sets is not a set.
2. Equivalence relations give rise to a partition by the set of equivalence classes.
3. For a Partition P of S, define an equivalence relation ~ by a~b if a and b are in the same element of P.
4. {1 2 3} has five partitions: three singletons, three possibilities to have one singleton and two dyads, and the triad.
5. {{1 2} {2 3}} gives rise to a reflexive and symmetric but not transitive relation. The classes are not disjoint.
6. Define ~ on **R** by a~b if b−a : **Z**. Then  **R**/~ is the same as **R**/**Z**, i. e. the circle. The 2-dimensional analog is a torus.

### 2. Functions between sets

* The restriction of a function f to a set S, denoted f|S, is given by f ◦ ι, where ι is the inclusion function from the domain of f to S.

* Injective functions are the ones with a left-inverse, surjections those with a right-inverse: Let f : A → B be injective, then there is a left-inverse that is an extension of i : im f → A. If f : A → B has a left-inverse i, it must be injective, otherwise there are x ≠ y such that f x = f y, but then x = i f x = i f y = y, a contradiction.
  Analogously for surjections.

   




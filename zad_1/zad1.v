Require Import Bool.
Lemma zad1_a : forall X Y : bool,
   (X && negb Y) || (negb X && negb Y) || (negb X && Y) = (negb X) || (negb Y).
Proof.
  intros X Y.
  destruct X, Y; simpl; reflexivity.
Qed.

Lemma zad1_b : forall X Y Z : bool,
  negb (X && Y && Z) && negb (negb X && Y && Z) && (X && negb Y && Z) = (X && negb Y && Z).
Proof.
  intros X Y Z.
  destruct X, Y, Z; simpl; reflexivity.
Qed.
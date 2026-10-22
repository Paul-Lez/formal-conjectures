/-
Copyright 2025 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-/
module

public import FormalConjecturesUtil

/-!
# Erdős Problem 143

*References:*
- [erdosproblems.com/143](https://www.erdosproblems.com/143)
- [Be35] Behrend, F., *On sequences of numbers not divisible by another*. J. London Math. Soc.
  (1935), 42-45.
- [KLL25] Koukoulopoulos, D., Lamzouri, Y. and Lichtman, J. D., *Erdős's integer dilation
  approximation problem and GCD graphs*. [arXiv:2502.09539](https://arxiv.org/abs/2502.09539)
  (2025).
- [Ap26] Apicella, Mattia, *A rational counterexample to the reciprocal-logarithmic assertion
  in Erdős problem 143* (2026).
  [Source linked by the problem page](https://github.com/mapice/erdos-143-candidate-disproof/tree/0f4b96940c97c7e0c36d17b584ec2bf1d842c02a)
-/

@[expose] public section

open Filter Finset
open scoped Topology

namespace Erdos143

/--
Let $A \subseteq (1, \infty)$ be a countably infinite set such that for all $x\neq y\in A$ and
integers $k \geq 1$ we have $|kx - y| \geq 1$.
-/
def WellSeparatedSet (A : Set ℝ) : Prop :=
  (A ⊆ (Set.Ioi (1 : ℝ))) ∧ Set.Infinite A ∧ Set.Countable A ∧
  (∀ x ∈ A, ∀ y ∈ A, x ≠ y → (∀ k ≥ (1 : ℕ), 1 ≤ |k * x - y|))

/--
Does this imply that
$$
\liminf \frac{|A \cap [1,x]|}{x} = 0?
$$
-/
@[category research open, question, AMS 11]
theorem erdos_143.parts.i : ∀ (A : Set ℝ), WellSeparatedSet A →
    liminf (fun x => (A ∩ (Set.Icc 1 x)).ncard / x) atTop = 0 := by
  sorry

/--
Does this imply that
$$
\sum_{x \in A} \frac{1}{x \log x} < \infty?
$$

The problem page records a negative answer, using the counterexample of Apicella [Ap26].
-/
@[category research solved, question, AMS 11]
theorem erdos_143.parts.ii :
    ¬ ∀ (A : Set ℝ), WellSeparatedSet A →
      Summable fun (x : A) ↦ 1 / (x * Real.log x) := by
  sorry

/--
Or
$$
\sum_{\substack{x < n \\ x \in A}} \frac{1}{x} = o(\log n)?
$$

This was proved by Koukoulopoulos, Lamzouri, and Lichtman [KLL25].
-/
@[category research solved, question, AMS 11]
theorem erdos_143.parts.iii : ∀ (A : Set ℝ), WellSeparatedSet A →
    (fun n : ℕ ↦ ∑ᶠ x ∈ A ∩ Set.Iio (n : ℝ), 1 / x) =o[atTop] (fun n : ℕ ↦ Real.log n) := by
  sorry

/--
Over the years Erdős asked for various different quantitative estimates, for example
$$
\liminf \frac{\lvert A\cap [1,x]\rvert}{x}=0
$$
or even (motivated by Behrend's bound [Be35])
$$
\sum_{\substack{x < n \\ x \in A}} \frac{1}{x} \ll \frac{\log x}{\sqrt{\log\log x}}.
$$

The variable $x$ on the right-hand side is read as $n$.
-/
@[category research open, question, AMS 11]
theorem erdos_143.variants.behrend_bound : ∀ (A : Set ℝ), WellSeparatedSet A →
    (fun n : ℕ ↦ ∑ᶠ x ∈ A ∩ Set.Iio (n : ℝ), 1 / x) =O[atTop]
      (fun n : ℕ ↦ Real.log n / Real.sqrt (Real.log (Real.log n))) := by
  sorry

end Erdos143

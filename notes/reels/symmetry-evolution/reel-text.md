# Symmetry and evolution — editable reel text

Five new reels from *Nature’s Improvisation on Symmetry*. This document is separate from the earlier Symmetry to Waves series.

The **Caption** fields are editable publication text, independent of the rendered videos. The **Title** fields record the approved titles and are checked against the generators. **On-screen text** records the wording baked into each video; changing it requires an update to the renderer and a new render. These lists are references, not rendering inputs. Dynamic numerical readings come from the animation.

The publication text is assembled in this order:

State and evolution · n/5
Title
Caption
Next: next reel’s title (Reels 01–04)
Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/
#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics

Caption limits include all these fields. Source notes are for offline review and are not posted.

Every video also displays its approved title, the shared brand “NATURE’S IMPROVISATION ON SYMMETRY,” the series label “STATE AND EVOLUTION  ·  n/5,” and “SYMMETRY.” The lists below record additional static scene text and equations; numerical clocks, matrix entries, sample numbers, and changing parameter values are omitted.

---

## Reel 01

### Title

Reversible evolution preserves information

### Caption

Two different preparations of a system remain different under reversible evolution. Each later state retains enough information to recover its own starting state.

The animation follows two arrangements of balls under the same laws. Each ball moves freely between elastic collisions with other balls or the walls. Run the evolution backward and each history retraces its course, returning to its own initial preparation.

Why must the states remain different? Suppose two distinct initial states evolved into exactly the same later state. Reversing the evolution would then have to recover two different starting states from one state, which would imply a loss of information.

A complete state here includes every ball’s position and velocity. A picture of positions alone can leave out the very information that distinguishes two preparations.

The final overlay places the two histories in one view so we can compare them. Each color still belongs to its own experiment, with its own collisions. What evolution preserves is the distinction between the complete states. The balls can travel, collide, and rearrange without erasing which preparation led to which outcome.

### On-screen text

- Two initial states · one reversible law
- Overlay of independent histories
- \Phi_{-t}\Phi_t=I
- State A
- State B
- ≠
- Distinct states remain distinct
- FORWARD
- BACKWARD
- PAUSED

### Source

Symmetry chapter, Unitarity discussion immediately before the reversible-histories animation. The caption spells out the inverse-map argument and includes velocities in the classical state. The overlay compares independent experiments; balls from different histories do not interact.

- [Source animation](../../../content/drafts/animations/symmetry-reversible-histories.mp4)
- [Source model](../../../scripts/symmetry_reversible_balls.py)
- [Source renderer](../../../scripts/generate_symmetry_reversible_histories.py)
- [Portrait renderer](../../../scripts/symmetry_evolution_reels/histories.py)

---

## Reel 02

### Title

Unitary evolution preserves overlap

### Caption

Unitary evolution preserves the similarity between wave states, even while their wave functions change shape.

The two colored surfaces show two alternative initial preparations undergoing the same evolution. Each surface plots the real part of a complex wave function. The waves spread and develop new patterns, but their inner product remains fixed:

⟨Uψ₁, Uψ₂⟩ = ⟨ψ₁, ψ₂⟩.

The inner product is a complex generalization of the dot product. To calculate it for wave functions, we multiply the complex conjugate of the first by the second and integrate over space. It compares the full complex functions, including their phases. Here its value stays at 0.40.

Setting both states in the equation equal also shows that each state keeps its norm. A normalized wave function stays normalized as it evolves.

In quantum mechanics, this preserves total probability. For normalized pure states, the magnitude of the overlap also tells us how well the two preparations can be distinguished by measurement. Orthogonal states have zero overlap and can be distinguished perfectly. Nonzero overlap limits that distinction. Applying the same unitary transformation preserves it.

At the end, the surfaces share one view so we can compare their shapes. They remain two alternatives. Running the evolution backward recovers both original states, with their overlap unchanged throughout.

### On-screen text

- Two initial states · one unitary evolution
- Overlay compares the two states
- \langle U\psi_A\mid U\psi_B\rangle=\langle\psi_A\mid\psi_B\rangle
- State A
- State B
- ≠
- Complex overlap  0.40 + 0.00i
- Surface height: Re ψ · fixed scale
- FORWARD
- BACKWARD
- PAUSED

### Source

Symmetry chapter, Unitarity discussion and the unitary-histories animation. The model evolves both normalized states with the same self-adjoint generator. The displayed overlap is the full complex inner product, not an overlap of probability densities or a comparison of the plotted real parts alone. Distinguishability is tied to its magnitude; unitarity preserves the complex value itself.

- [Source animation](../../../content/drafts/animations/symmetry-unitary-histories.mp4)
- [Source model](../../../scripts/symmetry_unitary_waves.py)
- [Source renderer](../../../scripts/generate_symmetry_unitary_histories.py)
- [Portrait renderer](../../../scripts/symmetry_evolution_reels/histories.py)

---

## Reel 03

### Title

Transforming an operator

### Caption

Like a vector, we can transform an operator. When an evolution operator acts on a generator, it tells us whether the symmetry transformation given by that generator is preserved under evolution. In this example, a stretch in one direction becomes a stretch in another direction when we conjugate it by a rotation.

Let A double the horizontal component of every vector while leaving its vertical component unchanged:

A(x, y) = (2x, y).

The square becomes a rectangle. The same rule acts on the entire grid, so we can see what A does to many vectors at once. Now let Uₛ be a rotation through an angle s. To transform the operator, we form

Aₛ = Uₛ†AUₛ.

Read this product from right to left. First Uₛ rotates the grid. Then A stretches it horizontally. Finally Uₛ† rotates it back. The dagger denotes the adjoint; for this rotation, it is the inverse. The two rotations would cancel if they were adjacent, but the directional stretch between them changes the result.

The complete sequence is another stretch operator, with its stretching direction turned clockwise through s. At s = 45°, it doubles components along one diagonal while leaving components along the perpendicular diagonal unchanged. Varying s turns those special directions continuously.

Here Uₛ is unitary: it preserves lengths and inner products. A doubles lengths along one direction, so A itself is not unitary. Conjugation lets us study how that operator changes under a unitary transformation. We are following the action of the stretch as its orientation changes.

### On-screen text

- Apply horizontal stretch
- Undo horizontal stretch
- A:\ (x,y)\longmapsto(2x,y)
- Horizontal stretch A
- A^\dagger A\ne I
- Rotate the grid, then rotate back
- U_s=R(s)
- Rotation Uₛ
- U_s^\dagger U_s=I
- Rotate 45° counterclockwise
- Apply the horizontal stretch
- Rotate back
- The complete operator
- Vary the rotation angle s
- A_s=U_s^\dagger A U_s
- Current grid map
- Transformed operator
- Rightmost factor acts first.
- The stretching direction changes with s.

### Source

Symmetry chapter, operator evolution before commutator preservation. The source uses A = diag(2, 1), Uₛ = R(s), and Aₛ = Uₛ†AUₛ. Positive s rotates the grid counterclockwise in the first step; the final operator’s stretching direction is clockwise relative to the original horizontal direction. At 45°, Aₛ has rows (1.5, −0.5) and (−0.5, 1.5). The stretch is not presented as unitary.

- [Source animation](../../../content/drafts/animations/symmetry-operator-sandwich.mp4)
- [Source model and renderer](../../../scripts/symmetry_stretch_operator_scenes.py)
- [Portrait renderer](../../../scripts/symmetry_evolution_reels/operators.py)

---

## Reel 04

### Title

Commuting operators

### Caption

A uniform stretch commutes with rotation. Stretch first and rotate afterward, or rotate first and stretch afterward: every vector reaches the same result.

This time A doubles every component:

A(x, y) = (2x, 2y), or A = 2I.

The symbol I denotes the identity operator, which leaves each vector unchanged. Multiplying it by two doubles every vector without selecting a preferred direction. Rotating those vectors before doubling them therefore gives the same result as doubling them before rotating.

For a rotation Uₛ, we can write this as AUₛ = UₛA. The difference between the two ordered products is the commutator:

[A, Uₛ] = AUₛ − UₛA = 0.

Now repeat the operator transformation from the previous reel: rotate the grid, apply A, and rotate back. Because A commutes with Uₛ, we can exchange their order in the product:

Aₛ = Uₛ†AUₛ = Uₛ†UₛA = A.

The rotations cancel and leave the original uniform stretch. Varying the rotation angle does not change the resulting operator. The grid may turn during the construction, but the complete transformation remains the same.

A directional stretch changes when its direction is turned. A uniform stretch has no preferred direction to turn. Commutation expresses this independence algebraically: the order of the two actions makes no difference.

### On-screen text

- Apply uniform stretch
- Undo uniform stretch
- A:\ (x,y)\longmapsto(2x,2y)
- Uniform stretch A
- A^\dagger A\ne I
- Rotate 45° counterclockwise
- Apply the uniform stretch
- Rotate back
- The complete operator
- Vary the rotation angle s
- A_s=U_s^\dagger A U_s
- Current grid map
- Transformed operator
- Rightmost factor acts first.
- [A,U_s]=0\quad\Longrightarrow\quad A_s=A

### Source

Symmetry chapter, the uniform-stretch example following the commutator equation for operator evolution. The source uses A = 2I and the same rotation convention as Reel 03. A commutes with every linear operator, hence with every rotation and its generator. The caption states the rotation case shown. A is not unitary; the rotation used to conjugate it is unitary.

- [Source animation](../../../content/drafts/animations/symmetry-uniform-operator-sandwich.mp4)
- [Source model and renderer](../../../scripts/symmetry_stretch_operator_scenes.py)
- [Portrait renderer](../../../scripts/symmetry_evolution_reels/operators.py)

---

## Reel 05

### Title

Information preservation and state-space geometry

### Caption

We can follow a family of wave packets through a simpler geometric picture by mapping each wave function to its average position and average wave number:

ψ ↦ (⟨X⟩, ⟨K⟩).

This view gives us a visual interpretation of information preservation. The six colored waves are samples from one chosen family. Their matching points locate them in the plane of averages. These two numbers describe where each sample lies in this family; they do not specify an arbitrary wave function.

Apply the same unitary evolution to every wave. In the example shown, their averages obey a linear map. First the patch shears: points with different average wave numbers shift by different amounts in position. Then it stretches along the position direction and compresses along the wave-number direction. Every grid cell follows a small region of the chosen family through these changes.

The patch changes shape while its area stays fixed. A shear can change a side’s length and angle without changing area; the squeeze shown scales the two coordinate directions by reciprocal factors. The geometry depends on both lengths and angles.

Meanwhile, the full wave functions retain all their pairwise complex overlaps. Reverse the operations in reverse order, and both the waves and their mapped patch return to the start.

This area-preserving map gives us a geometric view of this particular evolution. The cells mark regions of a continuous family, rather than counting quantum states. Preserving overlap is the full unitary statement; the moving patch shows how that evolution acts on these averages.

### On-screen text

- Map the waves to their averages
- Each cell follows a family of states
- Shear the patch and evolve the waves
- Stretch one direction, compress the other
- Reverse the evolution
- \psi\ \longmapsto\ (\langle\hat X\rangle_\psi,\langle\hat K\rangle_\psi)
- position x →
- \langle\hat X\rangle
- \langle\hat K\rangle
- Patch area
- same throughout
- A family whose averages shear and stretch together

### Source

Symmetry chapter, the mean-value patch after commutator preservation. The model is a family of displaced Gaussian packets acted on by a common free-propagation unitary followed by a squeeze. Its mean map is diag(exp(r), exp(−r)) × [[1, τ], [0, 1]], whose determinant is one. The source validates the complete complex Gram matrix, normalization, means, inverse evolution, and patch areas independently.

The patch is a map of this selected family to averages, not the full quantum state space. Grid cells follow subsets of the family; they are not individual states, uncertainty cells, or counts of distinguishable quantum states. The area statement is restricted to the linear mean evolution shown. It does not infer unitarity from area alone or require reciprocal side lengths under a general shear.

- [Source animation](../../../content/drafts/animations/symmetry-mean-patch.mp4)
- [Source model](../../../scripts/symmetry_mean_patch.py)
- [Source renderer](../../../scripts/generate_symmetry_mean_patch.py)
- [Portrait renderer](../../../scripts/symmetry_evolution_reels/geometry.py)

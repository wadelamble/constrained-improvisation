# Parallel transport — editable reel text

The caption can be edited independently of the video. Title and on-screen text are baked into the rendered frames.

### Title

The commutator encodes curvature

### Caption

Carry an arrow across a sphere in two different orders. Both routes reach the same point, but the arrows arrive pointing in different directions.

This is parallel transport. The arrow stays tangent to the sphere. Along each great-circle segment, it keeps the same angle to the direction of travel; at a corner, the route turns without turning the arrow.

Blue travels first in x, then in y. Gold reverses that order. At their common endpoint, the green arrow is the difference between the two results. That difference is the commutator acting on the initial arrow.

For small coordinate steps, the difference is approximately the product of the steps times the commutator of the transport generators. This is how the commutator encodes curvature. On a flat plane, the two transported arrows would agree.

Music: Herbie Hancock — Maiden Voyage (Remastered 2012).

### On-screen text

- NATURE’S IMPROVISATION ON SYMMETRY
- PARALLEL TRANSPORT
- The commutator encodes curvature
- Δv = [Tₓ(a), Tᵧ(b)]v
- Tₓ(a)Tᵧ(b)v − Tᵧ(b)Tₓ(a)v
- y, then x / x, then y
- One arrow. Two routes.
- Carry the arrow from A to B.
- The surface determines how it turns.
- First x, then y
- Keep the resulting blue arrow.
- Start again from A.
- Same initial arrow. Reverse the order.
- First y, then x
- Same endpoint. Different directions.
- In the tangent plane at B
- For small coordinate steps a and b:
- Δv ≈ ab[D̂ₓ,D̂ᵧ]v

### Source and validation

The reel reuses the exact gnomonic-coordinate construction in `scripts/generate_symmetry_parallel_transport_commutator.py`. Each coordinate leg is a great-circle arc. Blue is TᵧTₓv, gold is TₓTᵧv, and the green difference runs from the blue tip to the gold tip in a true orthonormal tangent frame. The finite operator commutator is exact; the generator relation is explicitly approximate for small steps.

The supplied Herbie Hancock recording is excerpted from 130 to 164 seconds, reduced by 4 dB, with a 1.5-second fade-in and a 2-second fade-out. The original audio file is unchanged.

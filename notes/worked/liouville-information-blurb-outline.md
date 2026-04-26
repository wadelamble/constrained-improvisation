# Liouville Information Blurb Outline

- Information does not belong to a single state in isolation.
- Information appears only relative to an ensemble, because only an ensemble weights some possible states more heavily than others.
- An ensemble of initial conditions is therefore information-bearing.
- If the ensemble has density `\rho(x)` on the space of states, then the realization of a particular state `x` carries surprisal `-\log \rho(x)`.
- Averaging that surprisal over the ensemble gives an exact scalar quantity, the Gibbs-Shannon entropy

```math
H[\rho] = -\int \rho(x)\log \rho(x)\,d\mu.
```

- This scalar quantifies the ensemble's average information content.
- But the scalar does not exhaust the ensemble's informational identity.
- Different densities can have the same entropy while encoding different distinctions among possible states.
- So the full informational identity of an ensemble lies in the entire density `\rho(x)`, that is, in the full pattern of weighted distinctions over the state space.
- That fuller structure is what later preservation claims must be about.
- The blurb may point forward to Liouville preserving that pattern, but should not try to prove preservation here.

## Danger Points

- Do not say that a single state carries information by itself. The information is always relative to an ensemble.
- Do not equate entropy with the whole informational identity of the ensemble.
- Do not slide from `natural measure on the state space` to `information` without the ensemble density in between.
- Do not claim preservation here. Only define what it would mean for information, or informational distinctions, to be preserved.

# HM Section Outline: From the Lagrangian to Canonical Momentum

## Increment 1: Section Target

- This section does **not** yet introduce the Hamiltonian as the main object.
- Its job is to show why Hamiltonian mechanics first reorganizes the instantaneous state by introducing canonical momentum.
- The motivating question is:
  - if LM already gives the physical path, what new structural need forces a change of variables at the level of the instantaneous state?
- The answer to aim at:
  - velocity is not yet the right partner for displacement if one wants a state description with a natural pairing, a natural boundary structure in the action, and a clean later passage to generator-based dynamics.

### Machine rationale

- Establishes the section's burden before symbols.
- Assumes `Why Another Mechanics?` and `What Is There Besides Paths?` have already motivated hidden structure in instantaneous state.
- Must not overclaim that canonical momentum is already symplectic structure in full.

## Increment 2: Why Velocity Is Not Enough

1. Start from what LM naturally gives at an instant:
   - configuration `q`
   - velocity `\dot q`
2. State the limitation carefully:
   - `\dot q` is path-rate data: it tells how configuration changes along a trajectory,
   - but the variational structure is asking a different question, namely what object answers to an infinitesimal displacement.
3. Sharpen the structural issue:
   - a displacement `\delta q` is a little move in configuration space,
   - to pair with such a move, one wants an object that acts linearly on displacements,
   - that is a dual object, not merely another tangent-like quantity.
4. So the transition is not:
   - “replace velocity with a handier variable”
5. It is:
   - “extract from the Lagrangian the dual object that answers to displacement.”

### Machine rationale

- This increment isolates the problem canonical momentum solves.
- Assumes reader already accepts that hidden structure should live in instantaneous state, not just along full histories.
- Must not start talking about phase space or symplectic area yet as if already established.

## Increment 3: The Action Boundary Term

1. Return to the action, because the pairing should come from the variational structure itself.
2. In varying the action, after integrating by parts, the endpoint term has schematic form

```math
\left.\frac{\partial L}{\partial \dot q^i}\,\delta q^i\right|_{t_1}^{t_2}.
```

3. This is the key structural fact:
   - the variational principle itself singles out `\partial L / \partial \dot q^i`
   - as the object that naturally contracts with a displacement `\delta q^i`
4. Therefore canonical momentum is not introduced by taste or by later hindsight.
5. It is already latent in the action as the object conjugate to displacement at the boundary.

### Machine rationale

- This is the strongest route to the human’s pressure point.
- Assumes willingness to use one variational formula.
- Must not yet say “therefore symplectic structure is proved”; only that the canonical pairing is already being selected here.

## Increment 4: Canonical Momentum As Dual Partner

1. Define canonical momentum only now:

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

2. Immediately interpret it structurally:
   - not first as `m v`
   - not first as “the momentum you already know from Newtonian mechanics”
   - but as the dual partner to `dq^i` selected by the action
3. State the geometric meaning in minimal terms:
   - `dq^i` is a displacement in configuration space
   - `p_i` is the object that pairs with it
   - together they already have the form of a conjugate pairing
4. Mention only lightly that in simple cases this reduces to familiar momentum, but that this is not the essence.

### Machine rationale

- This is where the section earns the word `canonical`.
- Assumes the boundary-term argument has already prepared the definition.
- Must not collapse back into “momentum is just mass times velocity.”

## Increment 5: Why This Is the Beginning of the Legendre Move

1. Now explain the conceptual role of the Legendre transformation without yet making the Hamiltonian the star.
2. The Lagrangian begins as a function of `q` and `\dot q`.
3. But once the action has singled out `p_i = \partial L/\partial \dot q^i`, the theory has identified a more structurally meaningful response variable to displacement.
4. The Legendre move is therefore:
   - not an arbitrary algebraic trick
   - but the re-expression of the state in terms of configuration and its canonically paired dual variable
5. Say explicitly:
   - the Legendre transformation is justified because the canonical pairing has already been exposed by the action.
   - the transform does not create that pairing; it re-expresses the state in terms of the variable the variation has already selected.
6. This is the strongest available answer to the question:
   - why is the Legendre move structurally the right move, rather than a mere change of variables after which useful geometry happens to appear?

### Machine rationale

- This is the conceptual payoff of the section.
- Assumes enough regularity that the Legendre map can actually be used.
- Must not overclaim that every later symplectic fact has already been proved here; only that the canonical pairing is not post hoc.

## Increment 6: Bridge Forward

1. End by stating what has now been achieved:
   - the instantaneous state is no longer best thought of as position plus velocity
   - it has been reorganized into displacement-plus-dual-response, that is, configuration plus canonical momentum
2. This is exactly the threshold needed for the next section.
3. The next section will say:
   - once the state is written in terms of `q` and `p`, phase space can be introduced cleanly
   - and the hidden geometry hinted at by Liouville can finally be named and formalized

### Machine rationale

- Gives the subsection a clean stopping point.
- Assumes the next section will pick up phase space explicitly.
- Must not prematurely import the symplectic formalism.

## Completed Reader-Facing Section Outline

1. Re-state the local problem.
   - Hamiltonian mechanics wants to reveal structure in the instantaneous state.
   - That requires more than `q` and `\dot q` as a mere kinematic snapshot.

2. Explain why velocity is not yet the right structural partner.
   - Velocity is path-rate data.
   - The variational structure asks instead for the object that answers to an infinitesimal displacement.
   - This points from tangent data toward dual data.

3. Return to the action and its variation.
   - Show the endpoint term after integration by parts.
   - Emphasize that `\partial L/\partial \dot q^i` is exactly what naturally contracts with `\delta q^i`.
   - This is where canonical momentum is being selected already.

4. Define canonical momentum.
   - `p_i = \partial L/\partial \dot q^i`
   - Interpret it first as the dual partner to displacement, not as inherited Newtonian momentum.

5. Explain why this is the beginning of the Legendre transformation.
   - The transform does not randomly produce useful variables.
   - The action variation has already exposed the conjugate object.
   - The Legendre move follows that prior structural fact.
   - Its real conceptual role is to reorganize the instantaneous state into configuration plus canonically paired dual variable.

6. Keep the Hamiltonian in the background.
   - Mention that this reorganization is what later permits the Hamiltonian formulation.
   - Do not yet make energy, first-order equations, or `H(q,p)` the main point.

7. Hand off to the next section.
   - Once the state is expressed in terms of `q` and `p`, the next section can introduce phase space and make its hidden geometry visible.

## Short Rationale Note

- Must show:
  - canonical momentum is introduced because the action already picks out the object conjugate to displacement,
  - the Legendre move is structurally motivated by that prior pairing rather than producing it from nowhere,
  - the section ends with `q,p` as an earned reorganization of state, ready for phase space.

- Must avoid:
  - reducing momentum to `m v`,
  - treating the Legendre transform as an algebra trick,
  - rushing to the Hamiltonian,
  - claiming the full symplectic structure has already been established.

- Strongest point:
  - the action boundary term, where `\partial L/\partial \dot q^i` appears paired with `\delta q^i`.

- Weakest point:
  - the move from `dual pairing appears in the variation` to `this is why the later phase-space geometry is the right one` remains partly promissory; it strongly earns the reorganization into `q,p`, but not the whole symplectic story yet.

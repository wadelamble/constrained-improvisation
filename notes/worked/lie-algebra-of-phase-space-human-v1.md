## Lie Alegebra of Phase Space

### Overview
There is a way to repackage Hamiltonian Mechanics as an algebra of functions on phase space which turns out to be valuable for several reasons:
1. It clarifies the objects in the theory and their structural relationships.
2. It provides a way of discovering theorems and relationships through algebraic manipulation, and in so doing makes new structure pop that otherwise is opaque.
3. While the nature of "physicality" and the underlying state space changes in quantum mechanics, the algebra describing Hamiltonian mechanics persists. This is critical because quantum mechanics is typically formulated in that algebra.

We will proceed as follows.
1. Understand what we mean by "an algebra"
2. Poisson Algebra
2.1 Understand how this algebra conceptually/geometrically is Lie algebra, which we have discussed already in reference to continuous symmetry.
2.1.1. Spaces of canonical transformations, which are flows \(something about 1-parameter\). 
2.1.2 Spaces of vector fields is "tangent" to space of canonical transformation, thus supports an algebra.
2.1.3. integrating diff q is like exponential map
2.1.4 Bridge is the [] -> {} identity
2.2 State the formal properties of the algebra \(which also makes this a Lie algebra\). 
2.2.1. What the algebra is on: functions
2.2.2. What the operations are including {}s
3. Things that pop.
4.1. {}s of any two functions.
4.2. Why we call these generator relationships
4.3. Noether's forward and reverse theorem.
4.4. Other? Bot?
5. Look ahead to quantum: from {} to [] and f to f-hat.

### What we mean by an algebra
We can express Hamiltonian mechanics as an algebra of functions on phase space. To say this clearly, we should first say what an algebra is. An algebra begins with some class of objects and then specifies two things: what operations may be performed on those objects, and what laws those operations satisfy. Different algebras may involve different objects, different operations, and different laws, but these differences still fall into a common taxonomy. Numbers with addition and multiplication are the familiar schoolroom example. Let us first examine that taxonomy, and then turn to the specific algebra relevant here.

#### Taxonomy of operations

| Category | Meaning | Example |
|---|---|---|
| Unary | Takes one input | Negation: $x \mapsto -x$ |
| Binary | Takes two inputs | Addition: $(x,y) \mapsto x+y$ |
| Internal | Takes allowed objects as input and returns another allowed object of the same kind | Sum of two functions is a function |
| External | Combines an allowed object with something outside the class | Scalar multiplication |

Algebras are "closed," meaning that when allowed objects are combined, the result is again an allowed object of the same kind.

#### Taxonomy of laws

| Category | Meaning | Example |
|---|---|---|
| Symmetry law | Governs what happens when inputs are swapped | Commutativity, antisymmetry |
| Grouping law | Governs what happens when an operation is repeated | Associativity |
| Linearity law | Governs behavior under sums and scalar multiples | Linearity, bilinearity |
| Compatibility law | Governs how two different operations interact | Distributive law, Leibniz rule |
| Consistency law | Governs deeper structural coherence | Jacobi identity |

### Poisson Algebra
We can now turn from this general taxonomy to the specific algebra built from functions on phase space called Poisson algebra. In Hamiltonian mechanics, the objects will be smooth functions on phase space. These include the familiar physical quantities position, momentum, energy, and angular momentum, but also arbitrary smooth functions with no associated physical observable. At the same time, these functions define vector fields on phase space under which the variation of any other function can be found. Through the algebraic lens, one may study not only the motion of states through phase space, but also the relationships in the full space of functions defined on it. The \"Poisson\" algebra is the structure that organizes these functions.

[Human] A Poisson algebra belongs to the broader class of Lie algebras that we mentioned when we discussed continuous symmetries. Lie algebra is built on the idea that while you cannot do an algebra on a curved space, you can do so on a flat tangent space to the curved space and then map the algebraic outputs to transformations on the curved space through an exponential map. In Poisson algebra, our group manifold is the space of canonical transformations (bot fill in there, what is a canonical transformation, example, notation) and our tangent space is the space of vector fields. in poisson algebra, there is one extra layer in addition to the tangent space and the group manifold, as the functions on phase space first generate the vector fields that are objects the tangent space using the procedure we have discussed. Note that "generate" is now used in two ways, somewhat sloppily -- functions generate vector fields, vector fields generate canoncial transformation. The lie algebra of the tangent space of vector fields is related to the lie algebra of functions by the identity  (bot: the [] = {} equation). This relation allows the algebraic relationships of the vector fields to persist in the relationships of the functions. In a standard Lie algebra, we would exponentiate generator matrices to generator parameterized flows. Here we integrate differential equations of the functions. these resolve to exponential maps as (bot: complete). Flows and canonical transformatin are related in that (bot: fill in). In a standard matrix generator / symmetry transformation lie algebra the canonical transformation analog would be (bot?) while the flow analog would be (bot) [End-human]

A Poisson algebra belongs to the broader class of Lie algebras. In the
usual symmetry setting, a Lie algebra is the tangent space at the
identity of a Lie group. The finite objects are the transformations
themselves. The infinitesimal objects are tangent vectors at the
identity, and the exponential map turns those infinitesimal generators
into one-parameter families of finite transformations.

[great. Please give a simplest-possible-example]

The Hamiltonian case has the same broad architecture, but with
different objects. The finite objects are canonical transformations,
that is, transformations of phase space that preserve the symplectic
form. [either say it in the previous paragraph or here. in the 'usual' setting, the transformations preserve some (distance-ish) invariant.] A one-parameter family of canonical transformations is a flow. [please provide an example with the right notation.]
The infinitesimal objects are vector fields on phase space. Integrating
such a vector field gives the corresponding flow. In this setting,
integration of a differential equation plays the same structural role
that exponentiation plays in the matrix picture [you didn't talk about matrixes as infintesimal generators above, you need to do so]: it turns an
infinitesimal generator into a finite transformation.

Poisson algebra has one extra layer not usually visible in the standard
matrix example. We do not usually write the infinitesimal generators
directly as vector fields. Instead, we write functions on phase space.
Each smooth function $f$ determines a vector field $X_f$, and that
vector field in turn determines a flow of canonical transformations. So
the chain of objects is

```text
function -> vector field -> flow -> canonical transformations.
```

This is the sense in which functions participate in a Lie algebra. They
do so not as isolated scalar labels ['scalar labels' is unclear to me], but through the vector fields they
generate. The bridge between the two levels is

```math
[X_f,X_g] = X_{\{f,g\}},
```

up to sign convention. The bracket on the left is the Lie bracket of
vector fields. The bracket on the right is the Poisson bracket of
functions. This identity says that the Lie algebra of infinitesimal
canonical transformations persists when one passes from vector fields to
the functions that generate them.


[give me a quick stepping back reflection like: "because we can work in the flat space of vector fields and then map to transoformation space, we can work in an algebra with its attendant abilities to make establishing relationships and theorems workaday." (for the love of god don't quote me)]

[Rewrite here]
A Poisson algebra belongs to the broader class of Lie algebras. In the
usual symmetry setting, the finite objects are transformations that
preserve some invariant quantity. For example, planar rotations preserve
the Euclidean length $x^2+y^2$, and may be written as a one-parameter
family of matrices $R_{\theta}$. The infinitesimal objects are the
generator matrices $A$ from which the finite transformations are built.
In that setting one writes

```math
R_\theta = e^{\theta A},
```

so exponentiation turns an infinitesimal generator into a
parameterized family of finite transformations.

The Hamiltonian case has the same broad architecture, but with
different objects. The finite objects are canonical transformations,
meaning transformations of phase space that preserve the symplectic
form. If we write one such family as $\phi_t$, then for each fixed
value of $t$ the map $\phi_t$ is one canonical transformation, while
the whole family $t \mapsto \phi_t$ is the flow. The infinitesimal
objects are vector fields on phase space. Integrating such a vector
field gives the corresponding flow. In this setting, integration of a
differential equation plays the same structural role that exponentiation
played in the matrix example: it turns an infinitesimal generator into a
finite transformation.

Poisson algebra has one extra layer not usually visible in the standard
matrix picture. We do not usually write the infinitesimal generators
directly as vector fields. Instead, we write functions on phase space.
Each smooth function $f$ determines a vector field $X_f$, and that
vector field in turn determines a flow of canonical transformations.
The word "generate" is therefore being used in two nearby senses:
functions determine vector fields, and vector fields determine flows.
The chain of objects is

```text
function -> vector field -> flow -> canonical transformations.
```

This is the sense in which functions participate in a Lie algebra. The
bridge between the vector-field level and the function level is

```math
[X_f,X_g] = X_{\{f,g\}},
```

up to sign convention. The bracket on the left is the Lie bracket of
vector fields. The bracket on the right is the Poisson bracket of
functions. This identity says that the Lie algebra of infinitesimal
canonical transformations persists when one passes from vector fields to
the functions that encode them.

The payoff is that one can work in the flat space of infinitesimal
generators rather than in the curved space of finite transformations.
That is what makes an algebra possible here, and it is what makes
relations and theorems available through algebraic manipulation.
[End rewrite here]

#### we'll get back to this
The first operations on this space are the obvious ones. Two functions may be added. A function may be multiplied by a scalar. Two functions may also be multiplied together pointwise to produce a third function. These operations already make the space of smooth functions into a familiar algebraic object. Hamiltonian mechanics adds one more binary internal operation, the Poisson bracket. It is this operation that encodes the specifically dynamical and generator-theoretic structure.

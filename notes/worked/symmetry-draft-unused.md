




#### Canonical commutator
In addition to all the palpable symmetry of nature and the fiber bundle structure that arises from the complex function representation, there is another symmetry group with altogether different and pivotal importance. This is symmetry group that stands behind Fourier transformations, known better by its commutator name than the symmetry group, the **canonical commutation relation**. Once we choose a complex wavefunction representation, one set of operators (for translation in $x$, $y$, $z$, and $t$) on the function space act to produce shifts in position and time. But a different set of operators produce shifts in wave number, and these operators do not commute. This failure to commute is not hard to show algebraically, but we will omit it. The effect of the commutator, that is, of shifting a wave in position, then in momentum, the completing the loop by undoing each operation, is to shift the phase of the wavefunction. 

```math
(T(a)\psi)(x)=\psi(x-a),
\qquad
(M(b)\widetilde\psi)(k)=\widetilde\psi(k-b).
```

Choosing the $x$-representation, the translation in $k$ becomes multiplication by a phase:

```math
(M(b)\psi)(x)=e^{ibx}\psi(x).
```

```math
T(a)M(b)T(-a)M(-b)
=
e^{-iab}I,
\qquad
[X,K]=iI.
```

The infinitesimal commutator can be exponentiated to obtain the finite phase advance:

```math
e^{-ab[X,K]}
=
e^{-iab}I.
```

So that:

```math
\left(e^{-iab}I\right)\psi(\bar{x})
=
e^{-iab}A e^{i\bar{k}\cdot\bar{x}}
=
A e^{i(\bar{k}\cdot\bar{x}-ab)}.
```

![Weyl order phase animation contact sheet](animations/differential-weyl-order-phase-contact-sheet.png)

*Applying position and wave-number shifts in opposite orders leaves a residual phase. The animation compares the inverse ordering, and therefore displays $e^{iab}$ rather than $e^{-iab}$.*

[Open MP4: differential-weyl-order-phase.mp4](animations/differential-weyl-order-phase.mp4)

We can write the phase of a wavefunction in terms of the time and position translation generators.

```math
\psi_{\mathbf k,\omega}(\mathbf x,t)
=
A e^{i(\mathbf k\cdot\mathbf x-\omega t)},
\qquad
-i\nabla\psi=\mathbf k\psi,
\qquad
i\partial_t\psi=\omega\psi.
```

$[X,K]$, then, tells us how phase advances, when applying the $\hat X$ and $\hat K$ operators interact when applied sequentially. But what does this mean? What does it mean to "apply the $\hat X$ operator" other than what we can say here, in the math itself, which is to transform the wavefunction along the $k$ axis. Because time and position translations commute, waves free state is to translate along $x$. However, waves do not freely change wave number over time. Thus "translation in wave number" doesn't freely happen over some time, making it yet harder to say what "applying the $\hat X$ operator" means.  

In quantum mechanics, indeed in wave mechanics in general, the information the wave carries is determined by the relative phases of its components. Shifting $k$ (or $x$ in the position representation) changes these relative phases, and the $[X,K]$ commutator tells us how a shift in $k$, and then in $x$ changes the shape of the wave function. But what, in practice, in physics, does it mean to shift the symmetry transformation's parameter? This is subtle. It is tempting to think that as a system evolves in time it is transformed along some symmetry. And this may we be the case if that symmetry is a symmetry of the system, such as transformation in position for a free particle. But a free wave certainly does not transform in $k$ space over time. The key to understanding the role of the commutator is to understand that the transformations are *hypothetical*. What we will see in a later is that path a system takes in time is the one for which some function on the path is **extremized**, that is, that it is minimized, maximized, or otherwise has a vanishing first derivative. To find the actual, physical path, we consider alternate paths between the same endpoints and ask how much they vary from alternate "wrong" paths. For a wave, as we will see later, this function is precisely the phase advance, and we can see how how rapidly the phase advance changes between candidate path by tiling the area they enclose with infinitesimal loops that contribute the value of the coummator. 

![A path variation tiled by local commutator loops](animations/symmetry-ccr-action-variation-contact-sheet.png)

[Open MP4: symmetry-ccr-action-variation.mp4](animations/symmetry-ccr-action-variation.mp4)

What have we said? That for travelling wave packets, the commutator encodes the actual, physical evolution of the packet. Once we have this, we can find the differential **equations of motion** which can be integrated to find the physical path, thus providing an alternate way to arrive at the real path. However, given the position and wave number generators and their commutator, we can directly derive the equations of motion without working out the **variational** procedure, as they are, precisely, the local measure of phase variation.

So much for waves, but why obsess about waves, or wave packets, or wavefunctions. The reason, which some may have guessed, is that in quantum mechanics, or we could say "the best mechanics we know," there are no particles or rigid objects with definite positions, but only probabilities of position and momentum measurements, which are encoded into a wavefunction. Thus in quantum mechanics the canonical commutation relation (CCR) along with the position and momentum (which is associated with wave number through Planck's constant, or $\hbar$) tells us the form of the equations of motion for *any* quantum system. 

...table of definitions...
...close...

#### Generators and Conserved Quantities
[move to function rep section - find a home...]
A generator is an operator. In a representation, it acts on a vector as a linear transformation. In the finite case, it is a matrix. However, in physics we associate generators with numerical quantities, and, in particular, with conserved quantities. For example, the operator $P_x$ generates translations in $x$, and it is associated with the conserved quanity $p_x$ in a system with translation symmetry in the $x$ direction. This relationship is best understood as an eigenvalue problem....

The clean bridge is to treat the possible positions of a point particle exactly as you treated the possible arrangements of cards or vertices of a triangle.

For every possible position $x$, introduce a formal basis vector

```math
|x\rangle.
```

A translation acts by permuting these definite-position vectors:

```math
T(a)|x\rangle=|x+a\rangle.
```

This is already a linear representation: define its action on linear combinations by linearity. Because there is now one coefficient for every possible value of $x$, a general vector has the form

```math
|\psi\rangle
=
\int dx\,\psi(x)|x\rangle.
```

The function $\psi(x)$ is simply the continuous coordinate list of that vector. Nothing quantum has been assumed. We have linearized the action of translations on the set of possible particle positions, just as a permutation representation linearizes the action on a finite set of vertices.

In the function coordinates, translation acts as

```math
(T(a)\psi)(x)=\psi(x-a).
```

Write

```math
T(a)=e^{-iaP}.
```

Differentiating at $a=0$ gives

```math
P=-i\frac{\partial}{\partial x}.
```

Now solve the eigenvalue problem:

```math
P\psi_p=p\psi_p.
```

Its solutions are

```math
\psi_p(x)=e^{ipx}.
```

Under a finite translation,

```math
T(a)\psi_p
=
e^{-iap}\psi_p.
```

So lowercase $p$ has a precise meaning:

> $p$ is the number measuring how a translation eigenvector responds to translation.

That explains why the generator and quantity use the same letter:

```math
P=\text{translation operator},
\qquad
p=\text{its eigenvalue}.
```

Now suppose the law of evolution respects translation symmetry. If $U(t)$ denotes evolution, then

```math
U(t)T(a)=T(a)U(t).
```

It therefore also commutes with the generator $P$. Starting with a $P$-eigenvector,

```math
P\psi_p=p\psi_p,
```

we obtain

```math
\begin{aligned}
P\,U(t)\psi_p
&=
U(t)P\psi_p\\
&=
p\,U(t)\psi_p.
\end{aligned}
```

Thus evolution may change the vector, but it cannot change its translation eigenvalue $p$. The number $p$ is conserved.

This gives the complete bridge using only the mathematics already available:

```math
\text{definite particle positions}
\longrightarrow
\text{basis vectors }|x\rangle
\longrightarrow
\text{function representation}
\longrightarrow
\text{translation operator }P
\longrightarrow
\text{eigenvalue }p
\longrightarrow
\text{conserved translation label}.
```

Physics calls that conserved translation label **momentum**.

One limitation should remain explicit: a definite-position vector $|x\rangle$ is not a momentum eigenvector. It decomposes into all the Fourier modes $\psi_p$. So this construction explains momentum as the conserved eigenvalue of translation, but it does not assign a definite momentum to an instantaneous point using its position alone. Motion or additional physical structure is needed for that.
[move to function rep section]

from intro...

The following synopsis looks ahead quite a bit, so we should not feel like we're missing something if it feels opaque at the moment. If we are to say that physical behavior has a given symmetry, we must be able to transform the equations that describe it along that symmetry. The equations of concern are differential equations, or more generally, **operator** equations, in which some operator takes in a function and returns a new function:

```math
g(x) = \hat O f(x)
```

In this view the "state being translated" is a function. If a function returns a number, or real scalar, its numerical values change under a symmetry transformation, but those values have no geometric content that must compose under the transformation. For example, if the transformation is rotation, numbers have no direction to rotate. However, functions can return vectors, matrices, or any other beast among the menagerie of mathematical objects. Those must also transform in some way that honors the composition rules of the symmetry, but as we will see momentarily, only certain mathematical objects are suited to **represent** a given symmetry. The mathematical objects we use as fundamental constituents in our equations must therefore be those that represent the symmetry. Symmetry constrains both the laws of evolution and the objects those laws act on.

 This could be a number, or a vector, or some other more exotic mathematical object. But whatever it is, when the function is transformed under a symmetry, such as rotated about a center point, the object the function returns must be transformed in its own right. For a simple number, there is no structure to transform, but an object like a vector that has an intrinsic orientation must itself transform in a way that abides by the symmetry.

![Vectors carry rotational symmetry](animations/symmetry-function-arrows-poster.png)

[Open MP4: symmetry-function-arrows.mp4](animations/symmetry-function-arrows.mp4)

*Vectors represent rotational symmetry*

Much as the vector as a mathematical object can be used to represent the rotational symmetry, the admissible objects in our theory must represent the symmetry from which it is constructed. 


For example, if we grant that a ball's state is specified by its position and velocity, Newton's first law that an object's velocity remains the same in the absence of external forces follows from position translation, rotation, and constant velocity symmetry. Consider that, if position and constant velocity symmetries are to hold, any change in velocity must be independent of the initial position or velocity. But then, if such a change existed, it would have to always point in the same direction, in contradiction of rotational symmetry. 


We will in due course introduce the following scheme. A "thing," otherwise known as a "fundamental particle," will have a state specified by a collection of statistical properties, such as the distribution of possible locations or velocities. Those statistical properties are encoded in a wave-like function. While such a function's amplitude yields probability distributions upon measurement, 

other aspects of it determine the type of thing whose properties are being measured. It is hard to preview these without getting into the material that lies ahead of us, but we can say the right words now and fill in their meaning as we go. First, the way a given function transforms limits it to 

the type of thing whose state is being measured is restricted in two ways, both of which are difficult to by the fixed way time, position, and velocity transformations relate for a given funcion and by the way the type of value the function returns -- for example, a vector -- behaves under rotations. The former determines the parameter we call a particle's mass, while the latter determines what we call its spin. These, along with other symmetry-derived parameters, identify the type of particle. This description is necessarily superficial at this point, but we will unpack it piece by piece.

First, the laws of physics must be consistent with the constraints symmetry imposes. Our pool table "acting the same way" under different symmetry **transformations** suggests that we may be able to construct quantities that are **invariant** under these transformations, such as, for example, the distance between our pool balls. Now suppose there were some quantity we could associate with every imaginable, wild way our pool balls could move to get from one particular starting state to another particular ending state, and imagine if the actual way they *do* move, the way that abides by the laws of physics, optimized this quantity. If this were the case, such a quantity would have to be an invariant of symmetry, for otherwise, a symmetry transformation would change these laws. As we will see, this is, in fact, the case, and the fact that the expression to be optimized, the **action**, must be an invariant of the symmetry makes "guessing" the quantitative expression for action a tractable problem it would otherwise not be.

#### The Role of Linear Operations on Function Representations
[maybe move this down a bit]
The function representation becomes indispensible when a "state" is thought of not as a single coordinate in state space, or the "state of a particle," but as a function, or distribution, over state space. In that case, treating distributions as vectors we evolve with operators allows us to define their overlap as an inner product. We can then require time evolution to be orthogonal, meaning that it preserves the lengths and angles between distribution vectors just as a rotation preserves the lengths and angles between ordinary vectors. That is:
```math
\langle O\rho_1,O\rho_2\rangle
=
\langle\rho_1,\rho_2\rangle.
```
The distributions may change as they evolve, but their overlap does not, so distinct distributions cannot be compressed together or collapse into the same distribution.

But why, we ask, should we focus on the evolution of a distribution of states rather than on a single state. In one sense, we might say the idea of a single state, an object at a point, is more a storytelling device than a scientifically-framed question. Questions like "how will this storm develop" or "how will voters react to inflation" don't start with a story about an individual air molecule or an indvidual voter, they ask to find patterns over spaces. More concretely, physics has two reasons to focus on te evolution of distributions. First, in the familiar world of "classical" mechanics, the number of individual states is often unfathomably large, so we instead study distributions characterized by aggregate properties. A hot system and a cool system, for example, correspond to different patterns distributed over state space. Their evolution is therefore naturally described as the transformation of one function over state space into another. This makes function representations—and linear operations that preserve the distinction between such functions—the appropriate language. Then, in the deeply unfamiliar world of "quantum" mechanics, individual states themselves become vectors in a function representation. At this point, only a linear operation that preserves inner products in the function space can describe even a single particle's evolution.

#### Fourier Decomposition of Wave Packets into Plane Wave Components
If you strike a chord on a piano, some complicated function of time describes how the sound pressure reaches your ear. It starts soft, gets louder, softens again. It has discernible main tones, but also a clutter of overtones that comprise the timbre of the piano. While you hear a clear tonal structure, a plot of the sound pressure level over time reaching your ear would completely obscure that structure. 

![Three-tone chord packet and its Fourier decomposition](animations/symmetry-fourier-three-tone-packet-contact-sheet.png)

[Open MP4: symmetry-fourier-three-tone-packet.mp4](animations/symmetry-fourier-three-tone-packet.mp4)

But we know something about this random-seeming function reaching your ear. We know it is comprised of mostly 3 pitches, and some overtones. If we plot the sound pressure level as a function of these pitches rather than as a function of time, the structure of our plot clearly reveals what we hear with our ear. "Pitch" is what we call a plane wave in music. The pattern of sound pressure over time is the sum of these pure **modes**. 

In fact, any smooth function that does not "blow up" as we go to positive or negative infinity, that is, any function whose inner product with itself is finite, can be decomposed into a linear combination, or **superposition** of plane waves. 

```math
\int_{-\infty}^{\infty}|f(x)|^2\,dx<\infty.
```

Physically, such a function is a **wave packet**. Expressing an arbitrary wave packet as a superposition of its modes is called **Fourier decomposition** and the transformation from an amplitude over translation coordinate to amplitude over wave number coordinate is called a **Fourier transformation**.

In modern physics, localizable objects are represented as wave packets. The story we want to tell is this -- nature's symmetry requires that the substrate of observations consists of combinations of "tones" and that the complexities that unfold over time are a way of perceiving the composition of these tones. Steep some tea, grab your crystals, and ponder -- the unfolding of nature in time, every child splashing in a puddle and every leaf falling from a tree, is, decomposed into its Fourier modes, a timeless "chord." Well, that's what the math says, anyway.

![A monochromatic Gaussian beam spreads less sideways as its wavelength decreases](animations/symmetry-monochromatic-gaussian-poster.png)

[Open MP4: symmetry-monochromatic-gaussian.mp4](animations/symmetry-monochromatic-gaussian.mp4)

*Shorter wavelengths reduce sideways diffraction*

---from ccr rewrite---

----unprocessed---
This invariance, as we've seen, is called unitarity. It preserves the distinguishability of states under symmetry transformations and makes those transformations reversible. When time evolution is itself unitary, the evolution of the state is deterministic and reversible. Translations in position and wave number preserve the inner product:

```math
\begin{gathered}
\text{Translation by }a\text{ in }x\\[0.5em]
\langle T_x(a)\psi,T_x(a)\chi\rangle\\
=\langle\psi,\chi\rangle,
\end{gathered}
\qquad
\begin{gathered}
\text{Translation by }b\text{ in }k\\[0.5em]
\langle T_k(b)\psi,T_k(b)\chi\rangle\\
=\langle\psi,\chi\rangle.
\end{gathered}
```


In addition to position and wave number, waves have a third independent way of changing. A wave's **phase**, $\phi$, refers to where it is in its cyclic pattern. For example, a phase shift of $2\pi$, or one full "cycle," returns the wave to its exact initial state. We need to be a bit careful here. For a pure mode, shifting its position is indistinguishable from shifting its phase, somewhat in the way the turning of a barbershop sign appears as though its stripes are moving up and down. We might, then, be tempted to think there is no difference between position and phase shifts. But the single mode is an idealization. In the general case, in which the wave function is a packet composed of modes, position translation shifts the entire function. Phase translation shifts each mode by the same fraction of its cycle, changing the function while leaving its magnitude envelope unchanged.



We can also discover and define phase directly from our symmetry group's commutation relations, which gives us a useful algebraic packaging of the group structure. Let's ask the question:

```math
[\hat X, \hat K] = \; ?
```

If the commutator is non-zero (and linearly independent of $\hat X$ and $\hat K$), there must be a third kind of transformation in the complete symmetry group. To find the commutator, we follow the usual procedure of translating the function around a loop in $x$-$k$ space and asking if the function changes. If it does, $?$ is nonzero, the commutator is the generator of that change, and the action will be identifiably that of a phase shift.

First, write a single mode in the $x$ and $k$ representations:

```math
\psi_{k_0}(x)
=
e^{ik_0x}.
```

```math
\begin{gathered}
\tilde{\psi}_{k_0}(k)=\sqrt{2\pi}\,\delta(k-k_0),\\[0.5em]
\text{where }\delta\text{ is a spike at }k_0\text{ that integrates to }1.
\end{gathered}
```

Define the $x$ and $k$ translation operators in their respective representations:

```math
(T_x(a)\psi_{k_0})(x)
=
\left(e^{-ia\hat K}\psi_{k_0}\right)(x)
=
\psi_{k_0}(x-a).
```

```math
(T_k(b)\widetilde\psi_{k_0})(k)
=
\widetilde\psi_{k_0}(k-b).
```

Working in the position basis,

```math
(T_k(b)\psi)(x)
=
\left(e^{ib\hat X}\psi\right)(x)
=
e^{ibx}\psi(x).
```

$\hat X$ generates translation in $k$-space just as $\hat K$ generated translations in $x$-space. In $x$-space, it multiplies $\psi$ by $x$ as it weights each component of $\psi$ by its position coordinate.

We can construct a loop by first translating the function by $b$ in $k$ and by $a$ in $x$, then by $-b$ in $k$ and by $-a$ in $x$.

```math
(T_x(a)T_k(b)\psi_{k_0})(x)
=
e^{i(k_0+b)(x-a)},
```

```math
(T_k(b)T_x(a)\psi_{k_0})(x)
=
e^{ibx}e^{ik_0(x-a)}.
```

```math
\bigl(T_x(-a)T_k(-b)T_x(a)T_k(b)\psi_{k_0}\bigr)(x)
=
e^{-ib(x+a)}e^{i(k_0+b)x}
=
e^{-ab[\hat X,\hat K]}\psi_{k_0}(x)
=
e^{-iab}\psi_{k_0}(x).
```

The two shifts fail to commute by the factor $e^{-iab}$. Writing $\phi=-ab$, the loop multiplies the function by $e^{i\phi}$. But this is precisely a phase shift, a rotation in the complex plane that “turns” the whole "spiral" of the wave function.

Because this factor is independent of $k_0$, the same phase shift applies to every mode in a superposition.

Phase translation, then, is a third translation symmetry, whose invariant is the inner product under its unitary action, rounding out the group of $x$, $k$, and $\phi$ coupled through their group structure:

```math
\langle T_x(a)\psi,T_x(a)\chi\rangle
=
\langle\psi,\chi\rangle.
```

```math
\langle T_k(b)\psi,T_k(b)\chi\rangle
=
\langle\psi,\chi\rangle.
```

```math
\langle T_\phi(\beta)\psi,T_\phi(\beta)\chi\rangle
=
\langle\psi,\chi\rangle.
```


The infinitesimal closed $x$-$k$ loop is generated by $[\hat X,\hat K]$. Because the finite loop leaves a phase translation, and phase translations are generated by $iI$, we have

```math
[\hat X,\hat K]
=
iI.
```

We might now ask, is phase a symmetry of physical behavior in the sense that position is? And what is its associated conserved quantity? For waves in everyday life, the answer is “sort of.” A change in phase can be detected by measuring the instantaneous wave value at a given place and time, but at the same time, typical observable properties like pitch and volume (or color and brightness if you prefer light to sound) are in fact the same under phase transformations. (Global phase is the common phase factor that multiplies all components in a packet. Changing relative phases between components can change interference and produce observable effects.) In the realm of quantum mechanics, however, global phase is completely undetectable. In fact, unlike position symmetry which frequently is broken when “external forces” are present, dynamical global phase symmetry is always present. And what, then, is its associated conserved quantity? It is the integral of a wave packet’s squared magnitude, which in quantum mechanics gives total probability. Once normalized to one, it remains one.

Mathematicians love to name groups. Just as we have encountered $D_3$ and $SO(2)$, our new group has a name, the three-dimensional Heisenberg group, or $H_3$. With $n$ spatial dimensions, the group has $2n+1$ dimensions, where the $+1$ is due to the fact that there is only one phase regardless of the number of spatial dimensions.

Before we close out here, a small amount of house cleaning is needed. First, we have not shown explicitly that changes in $\phi$ are linearly independent of changes in $x$ and $k$. They are, as evidenced by the fact that shifts in $\phi$ can leave the wave function's position and wave number unchanged. We also did not show that there are *only* 3 generators in $H_3$. This is done by showing that the generators close under commutation:

```math
[i\hat X,-i\hat K]=iI,
\qquad
[i\hat X,iI]=[-i\hat K,iI]=0.
```

---no---
We now have a representation space for translations, but what does this mean physically? When we translate a function, a wave packet, something physical translates in space. We needn't worry about this at the moment, but to make the statement concrete, we mean that we translate the probability density of detecting a particle. Once we ascribe physical significance to translation, we must also do so to the generator of translation. Now, if, by chance, the position translation operator and its generator are part of a symmetry group, with an associated commutation structure, that structure will constrain the physics of translation.
---no---


The transformation

```math
\psi(x)\;\longleftrightarrow\;\tilde{\psi}(k)
```

tells us that we can equally well translate a wave function  in $x$-space or in $k$-space. $k$-space is the dual, or equivalent up to role reversal, of $x$-space. Likewise, just as the $\hat K$ operator is the generator of postion translations, the $\hat X$ operator is the generator of wave-number translations. This coupled structure manifests by constraining the  evolution of the state. .....This coupled 

The transformation

```math
\psi(x)\;\longleftrightarrow\;\tilde{\psi}(k)
```

tells us that we can equally well translate a wave function  in $x$-space or in $k$-space. $k$-space is the dual, or equivalent up to role reversal, of $x$-space. Likewise, just as the $\hat K$ operator is the generator of postion translations, the $\hat X$ operator is the generator of wave-number translations. The greater $\hat K$, the more the function of x's value changes over a given a translation in positin ; the greater $\hat X$, the more a function of k's value changes over a change in wave-number. Now let this function be the time translation generator. in that case, the greater $\hat K$, greater the time rate change of x, and vice versa. this manifests as the familiar dV(x)/dx = dp/dt, dKE/dp = dx/dt.

Moreover, we will show that unitary evolution must preserve the commutator of these generators, which, as we will work out, means that ....

as the value one generator increases the other must decrease. (this is all messed up, but mabye we can save it)



---gone---
Fourier analysis follows from the structure of a symmetry group that acts on wave functions, the Heisenberg group, or $H_3$. $H_3$ is unitary, that is it preserves the inner product of states. Because the future of a system is determined by its current state, time evolution must
---gone----

---gone---
This group's actions preserve the overlaps between states, and therefore their distinguishability. They do not in general preserve the behavior of those states as they evolve. In this sense, they are symmetries of state space, whether or not they are also dynamical symmetries of a particular system. This group not only underlies Fourier analysis, but in defining similarity and distinguishability of wave functions, supplies an essential ingredient for a logically viable notion of state.
---gone---
----gone----
We can translate a wave function either in $x$-space or in $k$-space. While shifting the wave number isn't a translation in the familiar physical space we live in, from a mathematical perspective, $k$-space is the dual, or equivalent up to role reversal, of $x$-space. 
---gone----


From our discussion of Fourier analysis, we know that our state has a dual representation over wave number. The question we ask in physics, as always, is "how does a state evolve over time" which we can translate in our representation space view to "what operator evolves a state?" We require that the time evolution operator be unitary. Because positon and wave-number translation operators are unitary and form a basis for constructing possible operators on this state space, they are suitable building blocks for contructing such a unitary time evolution operator. Equivalently, position and wave-number generators can be used to construct a time evolution generator. Postion and wave-number translations are part of their own symmtry group, and, by constructing the time evolution generator from position and wave-number generators, we will ensure that evolution preserves the commutation relations of this symmetry group. The preservation of this structure will manifest in the form of equations of motion in which the rates of change of the position and wave-number generators are cross-coupled to the change of time evolution generator with respect to the dual Fourier generator.

---i think this is orphaend
For small shifts, the loop’s leading change is $-ab[\hat X,\hat K]\psi$. Here that change is $-iab\psi$. Therefore,

```math
[\hat X,\hat K]=iI.
```
--- end orphaned---

---no---
Because it is unitary, it will have a generator. We can treat the action this generator has on the state through the commutation relations between it and $D_3$ generators. 
---no----

---no---
First, consider the action any unitary operator, parameterized here by $s$, acting on any self-adjoint (unitary generating) operator. 
---no---
---remove or make work---
We can see this same result in another more intuitive way. We have identified the commutator with phase change, and phase change is just multiplication by a complex scalar, which can be performed before or after any linear operator with the same result:

```math
A(c\psi)=c\,A\psi.
```

Therefore, we know that whatever our time evolution operator is, it will necessary commute with preserve the $[\hat X, \hat K]. Thus while the equations of motion may or may not be preserved by changes to position (they are by spacetime symmetry in a free system) or changes to wave number (they generally are not), they must, by construction, be preserved under phase transformation. 

```math
U_t\!\left(e^{i\phi}\psi\right)
=
e^{i\phi}U_t\psi.
```
By linearity,

```math
A(c\psi)=c\,A\psi.
```
Given that the inner product is defined as:

The overlap between two complex wave functions is their **inner product**:

```math
\langle\psi_1,\psi_2\rangle
=
\int_{-\infty}^{\infty}\psi_1^*(x)\psi_2(x)\,dx,
```
where the star means complex conjugation so that multiplying a complex value by its conjugate gives its squared magnitude, a real number, we then have

```math
\begin{aligned}
\langle T_\phi\psi,T_\phi\chi\rangle
&=\int (e^{i\phi}\psi(x))^*(e^{i\phi}\chi(x))\,dx\\
&=\int e^{-i\phi}e^{i\phi}\psi(x)^*\chi(x)\,dx\\
&=\int\psi(x)^*\chi(x)\,dx\\
&=\langle\psi,\chi\rangle.
\end{aligned}
```





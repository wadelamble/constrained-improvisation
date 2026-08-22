Once we have a wavefunction representation of symmetry, we may note that we can move vectors (functions) in this space with operators that shift x, as we constructed, but also that shift k.  We thus recognize that our representation is also reprepresents a larger symmetry group, that of shifts in x and k. But unlike shifts in x, where mutliple dimensions commute, shifts in x and k do not commute.

Let

```math
\psi_k(x)=e^{ikx},
\qquad
(T_x(a)\psi)(x)=\psi(x-a),
\qquad
(T_k(b)\psi)(x)=e^{ibx}\psi(x),
```

where $T_x(a)$ shifts $x$ by $a$, while $T_k(b)$ shifts $k$ by $b$. Acting in the two possible orders,

```math
(T_x(a)T_k(b)\psi_k)(x)
=
e^{i(k+b)(x-a)},
```

but

```math
(T_k(b)T_x(a)\psi_k)(x)
=
e^{ibx}e^{ik(x-a)}.
```

Therefore

```math
T_x(a)T_k(b)\psi_k
=
e^{-iab}T_k(b)T_x(a)\psi_k,
```

so the two shifts fail to commute by the phase factor $e^{-iab}$.

But if the commutator is non-zero, this new, broader group, has an extra consitiuent-symmetry as well as we know know that the commutator is also a generator.  this constituent is the **phase** of the wave.

Indeed, completing the corresponding loop gives

```math
T_x(a)T_k(b)T_x(-a)T_k(-b)\psi
=
e^{-iab}\psi.
```

The wave returns to the same point in $(x,k)$, but with a changed phase. Infinitesimally, with

```math
\hat X\psi(x)=x\psi(x),
\qquad
\hat K\psi(x)=-i\frac{d\psi}{dx},
```

this becomes

```math
[\hat X,\hat K]=iI.
```

The operator $iI$ generates the additional central symmetry

```math
\psi\longmapsto e^{i\phi}\psi,
```

which is a uniform change of phase.

For a complex plane wave,

```math
\psi(x)
=
e^{i(kx+\phi)}
=
\cos(kx+\phi)+i\sin(kx+\phi).
```

At every $x$, its value is an arrow in the complex plane. Its phase is simply the angle $kx+\phi$ that this arrow makes with the positive real axis. As $x$ increases the arrow turns; changing $\phi$ rotates every arrow by the same amount.

Why do we bother to bring this esoteric seeming point up? The reason is that this [x,k] commutator that encodes phase change under a x,k space loop, and the phase change maps to physical **action** via a scale constant when we take the function representation seriously in quantum mechanics. Action, as we will see is the function that we "optimize" in a manner of speaking to find physically allowable paths, and from which physical generators -- momentum/position and time/energy -- gain their definitions.


The path a system takes in time is the one for which some function on the path is **extremized**, that is, that it is minimized, maximized, or otherwise has a vanishing first derivative. To find the actual, physical path, we consider alternate paths between the same endpoints and ask how much they vary from alternate "wrong" paths. For a wave, as we will see later, this function is precisely the phase advance, and we can see how how rapidly the phase advance changes between candidate path by tiling the area they enclose with infinitesimal loops that contribute the value of the coummator. 

![A path variation tiled by local commutator loops](animations/symmetry-ccr-action-variation-contact-sheet.png)

[Open MP4: symmetry-ccr-action-variation.mp4](animations/symmetry-ccr-action-variation.mp4)

What have we said? That for travelling wave packets, the commutator encodes the actual, physical evolution of the packet. Once we have this, we can find the differential **equations of motion** which can be integrated to find the physical path, thus providing an alternate way to arrive at the real path. However, given the position and wave number generators and their commutator, we can directly derive the equations of motion without working out the **variational** procedure, as they are, precisely, the local measure of phase variation.


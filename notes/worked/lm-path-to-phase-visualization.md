# Path to Phase Visualization

Picture a **phase dial**—a hand rotating around the unit circle—being carried along a candidate path in the $x$-$s$ plane.

For each small segment:

- moving horizontally by $\Delta x$ turns the dial by $k\Delta x$;
- moving vertically by $\Delta s$ turns it backward by $\omega\Delta s$;
- the net turn is

```math
\Delta\phi=k\Delta x-\omega\Delta s.
```

As you traverse the path, the dial retains its previous orientation and receives each additional turn. The integral

```math
\Phi[x,k]
=
\int(k\dot x-\omega)\,ds
```

is the dial's **total accumulated rotation**. Its final orientation is

```math
e^{i\Phi[x,k]}.
```

Different candidate paths between the same endpoints can leave the dial pointing in different directions. A stationary path is one for which slightly deforming the path produces almost no first-order change in that final direction.

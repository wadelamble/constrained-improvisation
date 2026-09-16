We’ll use $c=1$, and keep the wave description and the action description separate until we connect them.
1. Start with the joint wave function.

   ```math
   \Psi(K_1,K_2),
   \qquad
   K_i=(\omega_i,\mathbf k_i),
   \qquad
   \omega_i^2-|\mathbf k_i|^2=\kappa_i^2.
   ```

   $K_i$ specifies a mode. $\kappa_i$ labels the shell containing that mode.
2. The shell determines the proper-time phase rate.
   In the mode’s rest frame, $\mathbf k_i=0$, so $\omega_i=\kappa_i$. Coordinate time there is proper time. The mode becomes

   ```math
   e^{-i\kappa_i\tau_i},
   ```

   giving the accumulated free phase

   ```math
   \phi_i=-\kappa_i\tau_i.
   ```

   Thus $\kappa_i$ is the magnitude of the proper-time phase rate. No action or $\hbar$ has entered.
3. The shell also relates the wave mode to motion.
   The packet’s propagation velocity is

   ```math
   \mathbf v_i=\nabla_{\mathbf k_i}\omega_i
   =\frac{\mathbf k_i}{\omega_i}.
   ```

   In fourvector form, this gives

   ```math
   K_i^\mu=\kappa_i u_i^\mu.
   ```

   The fourvelocity $u_i$ has fixed spacetime magnitude, but its components can change.
4. Introduce an interaction respecting spacetime translations.
   The interaction evolves the joint wave function into amplitudes for different outgoing pairs. For our two-body channel, with each body retaining its shell label, every allowed transition satisfies

   ```math
   \Delta K_1^\mu=-\Delta K_2^\mu.
   ```

   This constrains quantum scattering outcomes; we have not assumed classical balls following definite collision trajectories.
5. The wave description therefore predicts relative recoil.
   Substitute $K_i^\mu=\kappa_i u_i^\mu$:

   ```math
   \kappa_1\Delta u_1^\mu
   +
   \kappa_2\Delta u_2^\mu
   =0.
   ```

   For equal and opposite exchanges, a larger $\kappa$ means a smaller change in fourvelocity.
   Changes of motion let us determine ratios of $\kappa$, without measuring phase. They do not determine the overall phase scale.
6. Now construct the action description of the same motion.
   Our earlier free-action construction gives, for each body,

   ```math
   S_i=-\alpha_i\tau_i.
   ```

   Each body has its own coefficient $\alpha_i$. At this point, we have not identified it with $\kappa_i$.
   These are the free contributions. The complete action also contains the interaction contribution.
7. The action coefficient also weights recoil.
   The free action supplies the translation quantity

   ```math
   \alpha_i u_i^\mu.
   ```

   Translation symmetry of the complete interaction therefore gives, between the incoming and outgoing free states,

   ```math
   \alpha_1\Delta u_1^\mu
   +
   \alpha_2\Delta u_2^\mu
   =0.
   ```

8. Match the two descriptions to the same changes of motion.
   We now have

   ```math
   \kappa_1\Delta u_1^\mu+\kappa_2\Delta u_2^\mu=0,
   ```

   and

   ```math
   \alpha_1\Delta u_1^\mu+\alpha_2\Delta u_2^\mu=0.
   ```

   For the same nonzero exchange, their relative weights must agree:

   ```math
   \frac{\alpha_i}{\alpha_{\rm ref}}
   =
   \frac{\kappa_i}{\kappa_{\rm ref}}
   =r_i.
   ```

   That is why we may write

   ```math
   \alpha_i=\alpha_{\rm ref}\,r_i.
   ```

   The reference coefficient is common; the individual coefficients are not.
9. Calibrate the common conversion.
   Choose a fixed mechanical normalization for $\alpha_{\rm ref}$. Then measure the reference body’s phase rate through interference between histories:

   ```math
   \Delta\phi_{\rm ref}
   =-\kappa_{\rm ref}\,\Delta\tau_{\rm ref}.
   ```

   The common conversion is

   ```math
   \boxed{
   \frac{\alpha_i}{\kappa_i}
   =
   \frac{\alpha_{\rm ref}}{\kappa_{\rm ref}}
   \equiv\hbar.
   }
   ```

   Choosing the reference unit is conventional. Measuring its phase rate supplies empirical information.
10. This connects action to phase.
    For the free contributions,

    ```math
    S_i=-\alpha_i\tau_i
    =-\hbar\kappa_i\tau_i
    =\hbar\phi_i.
    ```

    With the complete interaction law included and the same normalization applied to the whole history,

    ```math
    S[\gamma]=\hbar\phi[\gamma].
    ```

    The interaction terms require their interaction law; recoil alone does not supply them. And writing this relation does not change any phases—it connects two descriptions of them.
11. Phase differences determine the classical limit.
    Between candidate histories,

    ```math
    \Delta\phi=\frac{\Delta S}{\hbar}.
    ```

    When resolvable variations away from a stationary history sweep through action differences much larger than $\hbar$, their phases wind through many cycles. Their contributions cancel, leaving a narrow stationary neighborhood.
12. Now “increase $\hbar$ for the same body” has a precise meaning.
    Hold the mechanical description fixed—including the coefficients $\alpha_i$, the interaction, and the experimental geometry. Then

    ```math
    \kappa_i=\frac{\alpha_i}{\hbar}.
    ```

    Increasing $\hbar$ lowers the phase rates. The same resolvable variations produce fewer phase cycles, cancellation is less rapid, and quantum deviations remain visible over larger scales.
    Thus $\hbar$ sets how rapidly phase winds beneath a fixed mechanical description—and therefore the scale at which its stationary-motion approximation becomes adequate.

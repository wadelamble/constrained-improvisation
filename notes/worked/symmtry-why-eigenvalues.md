
#### The Importance of Eigenfunctions of Operators in Physics
[Comment:
1) move this whole section after fourier, it is a prereq
2) lose the die example
3) split existing fourier conversatin into fourier / qm]
Why should we care about eigenfunctions of operators? [comment: remove the next two sentences.]Often, a rote procedure can diagonalize a matrix, making subsequent matrix multiplication problems computationally tractable. This approach is pervasive in countless areas of engineering and data analysis due to its computational efficiency, but our interest is different. As we will discuss in detail later, in quantum mechanics, an ideal measurement results in a state "collapsing" to an eigenstate, and the value of the measurement is the corresponding eigenvalue.

To get a feel for this, consider rolling a die. As it tumbles in the air, the value is unknown until the "reveal operator" is applied and the die settles into a single face up. We can represent our "ignorance" by assigning equal probabilities to the six possible faces:

$$
\mathbf p=(p_1,p_2,p_3,p_4,p_5,p_6)
=\left(\frac16,\frac16,\frac16,\frac16,\frac16,\frac16\right).
$$

Next we can define an observable whose eigenvectors represent the possible faces and whose eigenvalues are their numerical values. Writing $|n\rangle$ for the basis vector associated with face $n$:

$$
\hat D=\sum_{n=1}^{6}n|n\rangle\langle n|
=\operatorname{diag}(1,2,3,4,5,6),
\qquad \hat D|n\rangle=n|n\rangle.
$$

The projector associated with outcome $n$ is $P_n=|n\rangle\langle n|$, while the probability of that outcome is simply the corresponding entry in our probability list:

$$
\Pr(n)=p_n=\frac16.
$$

The faces of the die are the eigenvectors of this operator and their values are the eigenvalues. 

This is surely an odd way to describe such a statistical situation, but it is, in fact, the way quantum mechanics formulates its predictions. There, the state is a complex-valued function over the eigenvalues of a given observable \(whose squared magnitude is the probability distribution over that observable.\) The difference between this theory and that of the die is that in the case of the die, thinking of the state as a superposition of possibilities was just a proxy for our ignorance about the "actual" state, whereas, in quantum mechanics, the notion that there is a physically definite state hidden by our ignorance is not the case in any ordinary sense similar to our die. The arguments for this are subtle and spectacular, and we will be best served to wait until we turn to quantum mechanics to give them their due, but if we take this idea of "existing in a superposition" on faith for the time being, then we have a compelling reason to study the eigenfunctions of operators in symmetry representations. 

[comment: change this paragraph to be just about 1) the object that is being translated being waves, and measured values being a fourier component, and 2) the "questions that can be asked") Skip casimir which has been covered. the rest has already been said.]
We've asserted that things that can be observed take the eigenvalues of operators on representations of nature's complete symmetry. This tells us several things. First, the only admissible questions the theory addresses are those that are represented by operators in a symmetry representation space. Second, the eigenfunctions of a given operator are a basis for the distribution of amplitudes over possible outcomes. Thus to know that the eigenfunction of the translation operator is a plane wave is to understand the essence of the very state that physics examines evolving over time. If someone were to ask "what is physics about?" we might reply "predicting the future from the current state." If then pressed, "state of what?" our answer would be "the state of a superposition of plane waves." Third, the referent of that state, the particle, is categorized by eigenvalues of operators that are invariant under symmetry transformation in a given irreducible representation.  That is, to "be an electron" is to inhabit an irreducible representation of dynamical symmetry that is labeled by the eigenvalues of Casimir operators (To be complete, the indentification also include charge values, whose origin we will describe later.) This expresses the truism that, in a theory that only answers questions that can be posed as operators on a symmetry representation, the kind of object something is must be invariant under that symmetry.

